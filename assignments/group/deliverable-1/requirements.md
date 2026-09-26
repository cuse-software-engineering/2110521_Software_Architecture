# Requirements

> Part of [Deliverable-1.md](Deliverable-1.md) — Concert Table Reservation System (2110521 Software Architecture).

## Functional Requirements

### User Authentication & Login System
- The system shall allow customers to authenticate using LINE Login.
- The system shall allow customers to access only their own reservations and digital tickets.
- The system shall authenticate all internal role accounts (Front Staff and Manager) with a username and password issued by the venue, separately from customer LINE Login.
- The system shall allow all users to log out securely.

### Venue Zone Map & Concert Round Management System
- The system shall allow admins to create and edit venue zone maps with zones, tables, table types, seating capacity and seat-view photographs, and to activate a map for use in concert rounds.
- The system shall validate a zone map before activation: every zone named and non-empty, table numbers unique, and every table with a table type, seating capacity and seat-view photograph.
- The system shall prevent the removal or relocation of a table that has confirmed bookings in a published concert round.
- The system shall allow managers to create a concert round with concert details, date, times and booking-open time, select an active zone map, mark tables not for sale, set package prices, table fees and the extra-person fee, and publish the round.
- The system shall validate a concert round before publishing and prevent overlapping published rounds.
- The system shall display real-time table availability, seat-view photographs, table type, seating capacity and zone for each table of a published concert round.

### Table Reservation System
- The system shall allow customers to select and reserve a specific available table.
- The system shall validate party size and prevent conflicting bookings.
- The system shall display reservation details, cutoff time, and booking conditions before confirmation.
- The system shall save confirmed reservations and update table availability.

### Digital Ticket & Check-In System
- The system shall generate a digital QR ticket for each confirmed reservation.
- The system shall allow customers to view their tickets in the web app.
- The system shall allow staff to scan tickets and confirm valid reservations.
- The system shall prevent invalid or duplicate check-ins and update checked-in tables to occupied.
- The system shall allow staff to update table statuses on the real-time floor plan.
- The system shall allow staff to assign an available table to a walk-in customer and record it as a walk-in booking.
- The system shall prevent a walk-in assignment to a table that is already held by a confirmed reservation.

### Arrival & Notification System
- The system shall send cutoff reminders through LINE.
- The system shall allow customers to select "I'm on my way" or request a 30-minute extension.
- The system shall allow staff to approve or reject extension requests and notify customers of the result.
- The system shall change the cutoff only after an extension is approved.
- The system shall expire reservations and release tables after the effective cutoff if customers have not checked in.

## Non-functional Requirements

### Operational
- The system shall support desktop and mobile devices.
- The customer web app shall operate within LINE Messenger on Android and iOS.
- The system shall back up reservation and venue data daily.

### Performance
- The system shall complete at least 95% of booking and QR validation requests within 2 seconds under a test load of 100 concurrent users, excluding external service and network delays.
- The system shall display table status updates within 3 seconds under normal network conditions.
- The system shall target monthly availability of at least 99.5%.

### Security
- The system shall verify customer identity through LINE Login.
- The system shall enforce role-based access for Manager, Staff, and Customer.
- The system shall use HTTPS and protect customer information and authentication credentials.
- The system shall prevent unauthorized access to reservations and digital tickets.

### Cultural and Legal
- The system shall provide a Thai-language interface.
- The system shall display booking and cutoff times using Thailand's local time zone.
- The system shall handle personal information in accordance with Thailand's PDPA and provide a privacy notice.

### Usability
- The system shall provide a responsive interface with clear navigation.
- The system shall clearly display table availability, cutoff times, and extension request statuses.
- The system shall provide understandable error messages.
- The system shall allow customers to retrieve their reservations and tickets easily.


