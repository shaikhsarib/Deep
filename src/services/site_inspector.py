import time
import logging
import hashlib
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from src.models.lead import AuditReport, BusinessProfile
from src.services.vertical_playbooks import detect_vertical, get_playbook, BusinessVertical

logger = logging.getLogger(__name__)

class SiteInspector:
    """
    Audits prospect websites for technical, mobile, and conversion flaws.
    Inspired by reverse-engineering techniques in REA (Chrome DevTools / CDP)
    and domain-specific conversion mechanics (Logistics, Events, Local SMBs).
    """

    def __init__(self, timeout: int = 8):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            )
        }

    def audit(self, profile: BusinessProfile) -> AuditReport:
        """Runs a complete technical & conversion audit on the business."""
        vertical = detect_vertical(profile.business_type, profile.company_name)
        profile.vertical = vertical.value

        if not profile.has_website or not profile.website:
            return self._audit_no_website(profile, vertical)
        
        return self._audit_live_website(profile, vertical)

    def _audit_no_website(self, profile: BusinessProfile, vertical: Optional[BusinessVertical] = None) -> AuditReport:
        """Audit for businesses operating without a website."""
        vert = vertical or detect_vertical(profile.business_type, profile.company_name)
        playbook = get_playbook(vert)

        if vert == BusinessVertical.LOGISTICS_TRANSPORT:
            flaws = [
                "No direct digital booking or freight rate calculator",
                "100% reliant on 3rd-party freight brokers and load boards (paying 15-25% broker cuts)",
                "Invisible to direct shippers searching online for reliable lane carriers",
                "No automated WhatsApp response system for after-hours rate inquiries"
            ]
            loss = "Losing 15-20% margin to freight brokers and ~8-12 spot loads weekly due to delayed manual quote turnaround"
        elif vert == BusinessVertical.EVENT_MANAGEMENT:
            flaws = [
                "No direct digital booking or date availability presence",
                "100% reliant on 3rd-party aggregators and directories (paying 20-30% platform cuts)",
                "Invisible to event planners searching late evening for venue confirmation",
                "No automated WhatsApp response system for after-hours inquiries"
            ]
            loss = "Losing 40-50% of high-intent wedding and corporate event inquiries arriving after-hours without instant date & package confirmation"
        else:
            flaws = [
                "No direct digital booking or ordering presence",
                "100% reliant on 3rd-party aggregators (paying 20-30% platform cuts)",
                "Invisible to high-intent Google searchers looking for official website",
                "No automated WhatsApp response system for after-hours inquiries"
            ]
            loss = "Losing 20-30% margin to aggregators and ~15-25 direct customer inquiries weekly"

        return AuditReport(
            load_time_seconds=None,
            has_ssl=False,
            is_mobile_responsive=False,
            has_whatsapp_widget=False,
            has_online_booking=False,
            key_flaws=flaws,
            quantified_loss=loss
        )

    def _audit_live_website(self, profile: BusinessProfile, vertical: Optional[BusinessVertical] = None) -> AuditReport:
        """Inspects live website via HTTP, SSL, and mobile DOM analysis."""
        vert = vertical or detect_vertical(profile.business_type, profile.company_name)
        playbook = get_playbook(vert)

        url = profile.website or ""
        if not url.startswith("http"):
            url = f"https://{url}"

        flaws: List[str] = []
        parsed = urlparse(url)
        has_ssl = parsed.scheme == "https"
        if not has_ssl:
            flaws.append("Missing SSL certificate (browsers warn visitors: 'Not Secure')")

        load_time: Optional[float] = None
        ttfb_seconds: Optional[float] = None
        raw_evidence_hash: Optional[str] = None
        html_text = ""
        is_mobile_responsive = False
        has_whatsapp_widget = False
        has_online_booking = False

        start_time = time.time()
        try:
            # Stream request to accurately measure Time-to-First-Byte (socket headers)
            ttfb_start = time.perf_counter()
            resp = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True, stream=True)
            ttfb_seconds = round(time.perf_counter() - ttfb_start, 3)

            # Consume full body to measure total page load
            _ = resp.content
            load_time = round(time.time() - start_time, 2)
            html_text = resp.text

            # Deterministic proof hash over raw response headers + status code
            raw_headers_bytes = f"{resp.status_code}:{sorted(resp.headers.items())}".encode("utf-8")
            raw_evidence_hash = hashlib.sha256(raw_headers_bytes).hexdigest()[:16]

            if load_time > 3.5:
                flaws.append(f"Slow mobile page load ({load_time}s, TTFB: {ttfb_seconds}s) — Google reports 53% of mobile visits abandon sites taking >3s")

            # Parse DOM
            soup = BeautifulSoup(html_text, "html.parser")

            # 1. Viewport check
            viewport_meta = soup.find("meta", attrs={"name": "viewport"})
            is_mobile_responsive = bool(viewport_meta)
            if not is_mobile_responsive:
                flaws.append("Missing mobile viewport configuration — layout breaks on smartphone screens")

            # 2. Meta description SEO
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if not meta_desc or not meta_desc.get("content"):
                flaws.append("Missing Google SEO meta description (reduces search snippet click-through rate)")

            # 3. WhatsApp Integration
            wa_links = soup.find_all("a", href=lambda h: h and ("wa.me" in h or "whatsapp" in h or "api.whatsapp" in h))
            has_whatsapp_widget = len(wa_links) > 0
            if not has_whatsapp_widget:
                flaws.append("No instant WhatsApp ordering/inquiry widget on landing page")

            # 4. Booking & Conversion check
            booking_triggers = ["book", "appointment", "reserve", "order online", "schedule"]
            booking_elements = soup.find_all(
                lambda tag: tag.name in ["button", "a", "form"] and any(t in tag.get_text().lower() for t in booking_triggers)
            )
            has_online_booking = len(booking_elements) > 0
            if not has_online_booking:
                flaws.append("No 1-click online booking or reservation system found")

            # 5. Domain-specific conversion checks
            if vert == BusinessVertical.LOGISTICS_TRANSPORT:
                freight_triggers = ["quote", "freight calculator", "rate estimator", "track shipment", "instant rate", "lane rates"]
                has_freight_tool = any(t in html_text.lower() for t in freight_triggers)
                if not has_freight_tool:
                    flaws.append("No instant freight rate calculator or live lane quote tool for shippers")
            elif vert == BusinessVertical.EVENT_MANAGEMENT:
                event_triggers = ["availability calendar", "check dates", "download brochure", "package pricing", "hall capacity"]
                has_event_tool = any(t in html_text.lower() for t in event_triggers)
                if not has_event_tool:
                    flaws.append("No real-time date availability checker or instant package brochure download")

        except requests.exceptions.SSLError:
            has_ssl = False
            flaws.append("Broken or expired SSL certificate")
        except Exception as e:
            logger.warning(f"Live audit error for {url}: {e}")
            flaws.append("Intermittent site downtime or sluggish DNS response")

        # Quantified loss calculation based on flaws found
        if len(flaws) >= 3:
            loss_statement = playbook.quantified_loss_template
        elif not has_whatsapp_widget or not has_online_booking:
            loss_statement = f"Losing high-intent {vert.value.replace('_', ' ')} clients weekly due to high friction in contact method"
        else:
            loss_statement = "Minor friction in mobile speed and search visibility"

        # Capture mobile visual screenshot proof (best-effort)
        screenshot_path = None
        try:
            from src.services.visual_auditor import visual_auditor
            # Use short slug or sanitized name
            slug = "".join(c for c in profile.company_name if c.isalnum() or c in "-_")[:30]
            screenshot_path = visual_auditor.capture_mobile_snapshot(url, lead_id=slug)
        except Exception as e:
            logger.debug(f"Visual auditor snapshot skipped: {e}")

        return AuditReport(
            load_time_seconds=load_time,
            ttfb_seconds=ttfb_seconds,
            has_ssl=has_ssl,
            is_mobile_responsive=is_mobile_responsive,
            has_whatsapp_widget=has_whatsapp_widget,
            has_online_booking=has_online_booking,
            key_flaws=flaws,
            quantified_loss=loss_statement,
            screenshot_path=screenshot_path,
            raw_evidence_hash=raw_evidence_hash
        )

site_inspector = SiteInspector()
