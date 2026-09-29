# Microservice Design

## 1. Scope of this deliverable

This document presents the first version of the microservice architecture for the Concert Table Reservation System (CTRS). It contains the Service–Operations–Collaborators table and the architecture diagram of the system, together with the reasoning that ties them to the three business use cases of Deliverable #1.

The architecture covers the three business use cases end to end, including their alternative and exceptional flows:

- **UC-01 Reserve a Specific Table** — the customer browses concert rounds, holds a table for 15 minutes, completes the profile, accepts the terms, pays the full table fee through the Payment Gateway and receives a QR e-ticket by LINE.
- **UC-02 Check In Using Digital QR Ticket** — Front Staff scans the e-ticket at the door, the booking reference is verified against the check-in window, the entry is confirmed and the table becomes occupied; bookings not checked in by the end of the grace period become no-shows.
- **UC-03 Create Concert Event** — the Manager creates a concert round on the venue zone map, prices the table types, validates and publishes it, which makes the round bookable in UC-01 and defines the check-in window used in UC-02.
- **UC-04 Create Venue Zone Map** — the Manager defines and names venue zones, places tables with unique table numbers, assigns table types and seating capacities, uploads seat-view photographs, validates and activates the map, which makes it selectable in UC-03 and provides the floor plan used in UC-01 and UC-02 for rounds that use it.

Maintaining the venue zone map is not itself one of the three business use cases. It appears in the architecture because a round cannot be created without it, and it is owned by the same service that owns the rounds.

## 1. Service–Operations–Collaborators

Operations are the business operations exposed by each service. Collaborators are the services or adapters that the service invokes to complete its own operations; an em dash means the service completes its work without calling anyone else.

| Service | Operations | Collaborators |
|---|---|---|
| **Concert Round Service** | createOrUpdateZoneMap()<br>setTableType()<br>uploadSeatViewPhoto()<br>createRound()<br>copyRound()<br>saveRoundAsDraft()<br>validateRound()<br>previewRound()<br>publishRound()<br>unpublishRound()<br>editPublishedRound()<br>getUpcomingRounds()<br>getRound()<br>getRoundTables()<br>getRoundPricing()<br>getCheckInWindow() | **Table Availability Service**<br>initializeRoundTableStatus()<br>**Booking Service**<br>getConfirmedBookingCount()<br>**Media Storage Adapter**<br>storeSeatViewPhoto() |
| **Table Availability Service** | initializeRoundTableStatus()<br>getRoundTableStatus()<br>holdTable()<br>extendHold()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>releaseTable()<br>publishTableStatusUpdate() | — |
| **Booking Service** | createHeldBooking()<br>setPartySize()<br>calculateTableFee()<br>saveCustomerProfile()<br>acceptBookingTerms()<br>startPayment()<br>confirmBookingPayment()<br>issueETicket()<br>getETicket()<br>cancelBooking()<br>getCustomerBookings()<br>findBookings()<br>checkInBooking()<br>recordAdditionalGuests()<br>escalateCheckIn()<br>resolveEscalation()<br>expireUnpaidBookings()<br>markNoShows()<br>getConfirmedBookingCount() | **Concert Round Service**<br>getRound()<br>getRoundPricing()<br>getCheckInWindow()<br>**Table Availability Service**<br>holdTable()<br>extendHold()<br>releaseHold()<br>markTableBooked()<br>markTableOccupied()<br>releaseTable()<br>**Payment Service**<br>createPaymentRequest()<br>requestRefund()<br>**Notification Service**<br>sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendRefundNotice() |
| **Payment Service** | createPaymentRequest()<br>receivePaymentResult()<br>getPaymentStatus()<br>pollPendingPaymentResults()<br>requestRefund()<br>submitTransferSlip()<br>reviewTransferSlip() | **Payment Gateway Adapter**<br>createCheckoutSession()<br>verifyWebhookSignature()<br>queryPaymentStatus()<br>refundPayment()<br>**Media Storage Adapter**<br>storeTransferSlip()<br>**Booking Service**<br>confirmBookingPayment() |
| **Notification Service** | sendBookingConfirmation()<br>sendHoldExpiredNotice()<br>sendRefundNotice()<br>sendSlipDecisionNotice()<br>retryFailedMessages()<br>getDeliveryStatus() | **LINE Messaging Adapter**<br>pushLineMessage() |

## Architecture diagram

![CTRS microservice architecture, version 1](../deliverable-2/assets/architecture-diagram.png)

*Figure 1  CTRS microservice architecture, version 1, drawn in the ports-and-adapters style: every service is a hexagon whose business logic is reached only through adapters on its edges. An arrow A → B means A invokes B; response paths are not drawn. The hosted checkout page of the Payment Gateway is opened by the customer's browser inside the web app and is therefore not shown as a service call.*
