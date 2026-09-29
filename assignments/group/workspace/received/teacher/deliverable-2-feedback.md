# Teacher feedback on Deliverable #2

Feedback from the teaching team on [Deliverable-2.pdf](../../../deliverables/report/Deliverable-2.pdf), kept as received. Score 2.0 / 2.0. Recorded 2026-09-29.

> คะแนน: 2.0/2.0 คะแนน
>
> Service–Operations–Collaborators: 1.0/1.0
>
> ส่งตารางครบถ้วน มีการระบุ operation และ collaborator อย่างละเอียด ครอบคลุมการจองโต๊ะ การตรวจสอบสถานะโต๊ะ การชำระเงิน การออก e-ticket การ check-in และการแจ้งเตือน เห็นความรับผิดชอบและ data ownership ของแต่ละ Service ชัดเจน
>
> Architecture Diagram: 1.0/1.0
>
> Diagram แสดง Actor, Service, Adapter, External System, data store และทิศทางการเรียกใช้งานได้ครบ ตารางกับ Diagram สอดคล้องกัน และแยกระบบภายนอก เช่น LINE, Payment Gateway และ Object Storage ได้เหมาะสม
>
> ข้อเสนอแนะด้าน Scope: ขอบเขตปัจจุบันมีทั้ง real-time table availability, payment/refund, QR check-in, notification, seat-view image และกรณีผิดพลาดจำนวนมาก ซึ่งค่อนข้างใหญ่สำหรับ 2–3 เดือน แนะนำให้ MVP รองรับการสร้างรอบคอนเสิร์ต การเลือกและจองโต๊ะ การชำระเงินแบบจำลอง และ QR check-in ก่อน ส่วน refund อัตโนมัติ, transfer-slip review, real-time WebSocket และ degraded payment mode ควรเป็นงานต่อยอด
>
> ภาพรวมออกแบบได้ละเอียดและมีความเชื่อมโยงระหว่าง Use Case กับ architecture ชัดเจนครับ

## Points to act on

- **FB-D2-01 Scope of the MVP.** For the 2–3 month build, the MVP should cover creating concert rounds, choosing and reserving a table, simulated payment and QR check-in. Automatic refunds, transfer-slip review, real-time WebSocket updates and the degraded payment mode become later increments. Done in the project document 2.0 draft 1: CH-03, CH-06, CH-14, CH-16, CH-19, CH-20. It affects the UC-01 flows, ADR-02 and the Payment and Table Availability services; see KI-06 and KI-07 in [../../notes/known-issues.md](../../notes/known-issues.md).
