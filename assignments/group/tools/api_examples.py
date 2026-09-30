#!/usr/bin/env python3
"""The example calls of Appendix D (one per screen, Tables D.1 to D.16), kept as data and rendered as coloured HTML into
workspace/report/project-document/07-appendices.md between the markers <!-- examples:ID --> and <!-- /examples -->.

    python3 tools/api_examples.py          # rewrite the blocks in the markdown

A call is call(request, *responses, headers=[...], body=obj); a response is ok/see/err(status, body, note). Bodies are
Python objects; the value ELL stands for the fields left out and prints as an unquoted ellipsis."""
import html
import json
import re
from pathlib import Path

GROUP = Path(__file__).resolve().parent.parent
MD = GROUP / "workspace" / "report" / "project-document" / "07-appendices.md"
ELL = "…"


def call(request, *responses, headers=(), body=None, note=None):
    return {"request": request, "headers": list(headers), "body": body, "responses": list(responses), "note": note}


def ok(status, body=None, note=None):
    return (status, body, note)


T = "→"   # the arrow before an answer

EXAMPLES = {
    "C1": [call("GET /api/rounds", ok(200, [ELL]), headers=["x-user-id: U-somchai", "x-role: customer"],
                note="progress 1; later Authorization: Bearer <LINE ID token> (ADR-01)")],
    "C2": [call("GET /api/rounds", ok(200, [{"id": "r-friday", "name": "Friday Live", "artist": "The Band", "date": "2026-10-09",
                                             "startAt": "2026-10-09T20:00:00Z", "bookingOpenAt": "2026-10-02T18:00:00Z",
                                             "status": "open", "availableTables": 28, "tablesForSale": 28}]))],
    "C3": [call("GET /api/rounds/r-friday/table-status", ok(304, None, "unchanged since version 4"),
                ok(200, {"roundId": "r-friday", "version": 5, "tables": [{"tableNumber": 1, "status": "HELD", "bookingId": "b-1", "holdEndsAt": "…T19:15:00Z"}, ELL]},
                   "ETag: 5"), headers=["If-None-Match: 4"]),
           call("POST /api/bookings", ok(200, {"id": "b-2", "status": "Held", "tableNumber": 2, "remainingHoldSeconds": 900, ELL: ELL}),
                ok(409, {"error": "the table has just been taken by another customer"}, "UC-01 AF-3"), body={"roundId": "r-friday", "tableNumber": 2})],
    "C4": [call("PUT /api/bookings/b-2/party-size", ok(200, {"id": "b-2", "status": "Held", "partySize": 3,
                                                             "fee": {"packagePrice": 2400, "extraPersons": 1, "extraPersonFee": 600, "fullTableFee": 3000}, ELL: ELL}),
                body={"partySize": 3}),
           call("POST /api/bookings/b-2/cancel", ok(200, {"id": "b-2", "status": "Cancelled", "history": [ELL, {"status": "Cancelled", "by": "U-somchai", ELL: ELL}], ELL: ELL}))],
    "C5": [call("GET /api/customers/me", ok(404, {"error": "no profile yet: this is the first booking"})),
           call("POST /api/customers/me", ok(200, {"customerId": "U-somchai", "name": "Somchai P.", "phone": "0812345678", "consentAt": "2026-10-03T12:00:00Z"}),
                ok(400, {"error": "invalid profile", "details": ["phone must be a Thai mobile number"]}, "UC-09 AF-2"),
                body={"name": "Somchai P.", "phone": "0812345678", "consent": True})],
    "C6": [call("GET /api/bookings/b-2/terms", ok(200, {"bookingId": "b-2", "terms": ["Full payment confirms the booking; …", ELL],
                                                       "checkInWindow": {"opensAt": "2026-10-09T18:00:00Z", "startAt": "2026-10-09T20:00:00Z", "graceEndsAt": "2026-10-09T20:30:00Z"}})),
           call("POST /api/bookings/b-2/terms-acceptance", ok(200, {"id": "b-2", "status": "Held", "termsAccepted": True, ELL: ELL}))],
    "C7": [call("POST /api/bookings/b-2/payment", ok(200, {"paymentId": "p-7", "checkoutUrl": "https://checkout.example/pay/p-7"}),
                ok(501, {"error": "startPayment() is built in progress 2"}, "Increment 1")),
           call("GET /api/payments/p-7", ok(200, {"paymentId": "p-7", "bookingId": "b-2", "status": "Paid", "amount": 3000}), note="polled until the result")],
    "C8": [call("GET /api/bookings/b-2", ok(200, {"id": "b-2", "status": "Confirmed", "tableNumber": 2, "zoneName": "Zone A", "partySize": 3, "fee": {ELL: ELL, "fullTableFee": 3000}, ELL: ELL})),
           call("GET /api/bookings/b-2/e-ticket", ok(200, {"bookingId": "b-2", "bookingReference": "SEATS-261009-A02-7K3Q", "qrPayload": ELL}))],
    "C9": [call("GET /api/customers/me/bookings", ok(200, [{"id": "b-2", "roundId": "r-friday", "tableNumber": 2, "status": "Confirmed", ELL: ELL},
                                                           {"id": "b-1", "roundId": "r-sat", "tableNumber": 9, "status": "Expired", ELL: ELL}]))],
    "B1": [call("POST /api/sessions", ok(200, {"token": "5e1f…", "role": "manager", "staffAccountId": "s-1"}),
                ok(401, {"error": "wrong username or password"}), body={"username": "manager", "password": "…"}),
           call("DELETE /api/sessions/current", ok(200), headers=["Authorization: Bearer 5e1f…"])],
    "B2": [call("POST /api/zone-maps", ok(200, {"id": "m-2", "name": "Main hall v2", "status": "Draft", "imageUrl": "", "zones": [], "tables": [], "summary": [], ELL: ELL}), body={"name": "Main hall v2"}),
           call("PUT /api/zone-maps/m-2", ok(200, {"id": "m-2", "status": "Draft", "zones": [{"id": "A", "name": "Zone A · front stage"}],
                                                  "tables": [{"tableNumber": 1, "zoneId": "A", "tableTypeId": "round2", "capacity": 2, "x": 40, "y": 60}],
                                                  "summary": [{"zoneId": "A", "name": "Zone A · front stage", "tables": 1, "capacity": 2}], ELL: ELL}),
                body={"zones": [{"id": "A", "name": "Zone A · front stage"}], "tables": [{"tableNumber": 1, "zoneId": "A", "tableTypeId": "round2", "capacity": 2, "x": 40, "y": 60}]}),
           call("POST /api/zone-maps/m-2/validate", ok(200, {"valid": False, "problems": ["table 17 has no table type", "the zone containing table 17 has no name"]}), note="UC-04 S-1"),
           call("POST /api/zone-maps/m-2/activate", ok(400, {"error": "the zone map is not valid", "details": ["table 17 has no table type", ELL]}),
                ok(200, {"id": "m-2", "status": "Active", ELL: ELL}, "once valid")),
           call("PUT /api/table-types/round2", ok(200, {"id": "round2", "name": "2-person round table", "capacity": 2, "packageContent": "1 tower + 1 ice"}),
                body={"name": "2-person round table", "capacity": 2, "packageContent": "1 tower + 1 ice"})],
    "B3": [call("POST /api/rounds", ok(200, {"id": "r-friday", "name": "Friday Live", "status": "Draft", "checkInWindow": None, "parameters": None, "tables": [], ELL: ELL}), body={"name": "Friday Live"}),
           call("PUT /api/rounds/r-friday", ok(200, {"id": "r-friday", "status": "Draft", "artist": "The Band", "date": "2026-10-09", "zoneMapId": "m-1", "tablesNotForSale": [6],
                                                     "checkInWindow": {"opensAt": "2026-10-09T18:00:00Z", "startAt": "2026-10-09T20:00:00Z", "graceEndsAt": "2026-10-09T20:30:00Z"},
                                                     "tables": [{"tableNumber": 1, "zoneId": "A", "tableTypeId": "sofa6", "capacity": 6, "forSale": True, "packagePrice": 7200, ELL: ELL}, ELL], ELL: ELL}),
                ok(409, {"error": "after the booking-open time these fields are fixed: zoneMapId", "details": {"confirmedBookings": 12}}, "a Published round, UC-03 AF-3"),
                body={"artist": "The Band", "date": "2026-10-09", "doorsOpenAt": "2026-10-09T18:00:00Z", "startAt": "2026-10-09T20:00:00Z", "bookingOpenAt": "2026-10-02T18:00:00Z",
                      "zoneMapId": "m-1", "tablesNotForSale": [6], "prices": [{"zoneId": "A", "tableTypeId": "sofa6", "packagePrice": 7200, "packageContent": "3 towers + 3 ice"}, ELL]}),
           call("POST /api/rounds/r-friday/validate", ok(200, {"valid": False, "problems": ["no package price for table type seat1 in zone B"]}), note="UC-03 S-1"),
           call("POST /api/rounds/r-friday/publish", ok(200, {"id": "r-friday", "status": "Published", "parameters": {"holdPeriodMinutes": 15, "checkInWindowHours": 2, "gracePeriodMinutes": 30, "extraPersonFee": 600}, ELL: ELL}),
                ok(400, {"error": "the round is not valid", "details": [ELL]}), note="creates the table map of the round; idempotent")],
    "B4": [call("GET /api/rounds/r-friday/table-status", ok(304, None, "unchanged since version 41; the 200 answer is that of C3"),
                headers=["If-None-Match: 41"], note="polled every 2 seconds"),
           call("GET /api/rounds/r-friday/bookings", ok(200, [{"id": "b-2", "tableNumber": 1, "partySize": 3, "status": "Checked-in", ELL: ELL}, ELL]))],
    "B5": [call("POST /api/check-ins/verify", ok(200, {"valid": True, "booking": {"id": "b-2", "tableNumber": 1, "zoneName": "Zone A", "partySize": 3, "status": "Confirmed", ELL: ELL}, "reason": ""}),
                ok(200, {"valid": False, "booking": None, "reason": "already checked in at 19:42 by door1"}, "UC-02 EF-1"),
                ok(501, {"error": "verifyBookingReference() is built in progress 2"}, "progress 1"),
                body={"bookingReference": "SEATS-261009-A02-7K3Q"})],
    "B6": [call("POST /api/check-ins", ok(200, {"id": "b-2", "status": "Checked-in", "history": [ELL, {"status": "Checked-in", "at": "2026-10-09T19:05:00Z", "by": "door1"}], ELL: ELL}),
                ok(501, {"error": "checkInBooking() is built in progress 2"}, "progress 1"), body={"bookingReference": "SEATS-261009-A02-7K3Q"})],
    "B7": [call("GET /api/business-parameters", ok(200, {"holdPeriodMinutes": 15, "checkInWindowHours": 2, "gracePeriodMinutes": 30, "extraPersonFee": 600})),
           call("PUT /api/business-parameters", ok(200, {"holdPeriodMinutes": 15, "checkInWindowHours": 2, "gracePeriodMinutes": 30, "extraPersonFee": 700}), body={"extraPersonFee": 700}),
           call("GET /api/staff-accounts", ok(200, [{"staffAccountId": "s-1", "username": "manager", "role": "manager", "status": "Active"},
                                                   {"staffAccountId": "s-2", "username": "door1", "role": "front_staff", "status": "Active"}, ELL])),
           call("POST /api/staff-accounts", ok(200, {"staffAccountId": "s-4", "username": "door2", "role": "front_staff", "status": "Active"}),
                ok(409, {"error": "username door2 is taken"}), body={"username": "door2", "role": "front_staff", "password": "…"}),
           call("DELETE /api/staff-accounts/s-4", ok(200, {"staffAccountId": "s-4", "username": "door2", "role": "front_staff", "status": "Disabled"}))],
}


# ------------------------------------------------------------------------------------------------------------ rendering
WIDTH = 92   # a structure that fits in one line stays on one line; longer ones open up, one field per line


def _json(obj, indent: int = 0) -> str:
    """Pretty-printed JSON that stays compact: short objects and arrays on one line, long ones one member per line."""
    flat = json.dumps(obj, ensure_ascii=False, separators=(", ", ": "))
    if len(flat) + indent <= WIDTH or not isinstance(obj, (dict, list)):
        text = flat
    else:
        pad = " " * (indent + 2)
        if isinstance(obj, dict):
            items = [pad + ELL if k == ELL else f'{pad}{json.dumps(k, ensure_ascii=False)}: {_json(v, indent + 2)}' for k, v in obj.items()]
            text = "{\n" + ",\n".join(items) + "\n" + " " * indent + "}"
        else:
            items = [f"{pad}{_json(v, indent + 2)}" for v in obj]
            text = "[\n" + ",\n".join(items) + "\n" + " " * indent + "]"
    return text.replace(f'"{ELL}": "{ELL}"', ELL).replace(f'"{ELL}"', ELL)   # the fields left out


TOKEN = re.compile(r'("(?:[^"\\]|\\.)*")(\s*:)?|(-?\d+(?:\.\d+)?)|\b(true|false|null)\b|(…)')


def _colour(text: str) -> str:
    """Syntax colouring of pretty-printed JSON: keys, strings, numbers, keywords, the ellipsis."""
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        if m.group(1):
            cls = "k" if m.group(2) else "s"
            out.append(f'<span class="{cls}">{html.escape(m.group(1))}</span>{html.escape(m.group(2) or "")}')
        elif m.group(3):
            out.append(f'<span class="n">{m.group(3)}</span>')
        elif m.group(4):
            out.append(f'<span class="b">{m.group(4)}</span>')
        else:
            out.append('<span class="el">…</span>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


def _status_class(status: int) -> str:
    return "ok" if status < 300 else ("redir" if status < 400 else "err")


def render(sid: str) -> str:
    blocks = []
    for c in EXAMPLES[sid]:
        method, path = c["request"].split(" ", 1)
        lines = [f'<span class="rq"><span class="m">{method}</span> {html.escape(path)}</span>' + (f'   <span class="note">{html.escape(c["note"])}</span>' if c["note"] else "")]
        lines += [f'<span class="hd">{html.escape(h)}</span>' for h in c["headers"]]
        if c["body"] is not None:
            lines.append(_colour(_json(c["body"])))
        for status, body, note in c["responses"]:
            head = f'{T} <span class="{_status_class(status)}">{status}</span>' + (f' <span class="note">{html.escape(note)}</span>' if note else "")
            lines.append(head if body is None else head + "\n" + _colour(_json(body)))
        blocks.append('<span class="call">' + "\n".join(lines) + "</span>")
    return '<pre class="calls">' + "\n\n".join(blocks) + "</pre>"


def write() -> None:
    text = MD.read_text(encoding="utf-8")
    count = 0
    for sid in EXAMPLES:
        block = f"<!-- examples:{sid} -->\n{render(sid)}\n<!-- /examples -->"
        marked = re.compile(rf"<!-- examples:{sid} -->.*?<!-- /examples -->", re.S)
        if marked.search(text):
            text = marked.sub(lambda _m: block, text, count=1)
        else:   # first run: the old <pre class="call"> of the screen's block
            i = text.index(f"Screen {sid},")
            j = text.index('<pre class="call">', i); k = text.index("</pre>", j) + len("</pre>")
            text = text[:j] + block + text[k:]
        count += 1
    MD.write_text(text, encoding="utf-8")
    print(f"wrote {count} example blocks into {MD.relative_to(GROUP)}")


if __name__ == "__main__":
    write()
