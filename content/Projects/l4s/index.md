---
title: Experience-Driven L4S Internet Service Architecture in FreeBSD

summary: A research project enhancing low-latency, lossless, and scalable internet service delivery using the FreeBSD networking stack.

abstract: |
  This project, supported by the APNIC Foundation, focuses on implementing the IETF-defined L4S (Low Latency, Low Loss, Scalable Throughput) architecture within the FreeBSD kernel to support real-time, congestion-aware internet applications. The work involves modifying queue management systems and using reinforcement learning to dynamically optimize performance for modern digital services including cloud gaming, real-time video, and industrial IoT.

date: 2025-05-12

featured: true

image:
  caption: 'Implementation of L4S in FreeBSD for next-generation low-latency networking.'
  focal_point: Right
  filename: l4s-networking.jpg

projects: []

tags: ["L4S", "FreeBSD", "Internet Architecture", "Networking", "QoS", "QoE"]

url_pdf: ""
url_slides: ""
url_code: ""
url_video: ""
external_link: "https://apnic.foundation/projects/implementing-an-experience-driven-l4s-internet-service-architecture-in-freebsd/"
---

The **Deakin IoT Lab** in collaboration with the **APNIC Foundation** is implementing an **experience-driven L4S Internet Service Architecture** in FreeBSD. This work is aligned with IETF’s RFC 9330 and aims to modernize the internet’s congestion management for applications demanding ultra-low latency.

The solution incorporates:
- A dual-queue coupled Active Queue Management (AQM) system
- Real-time dynamic optimization using reinforcement learning (A3C)
- Evaluation in high-throughput environments with latency-sensitive use cases

For more details, visit the [official project page](https://apnic.foundation/projects/implementing-an-experience-driven-l4s-internet-service-architecture-in-freebsd/).