# Product Requirements Document (PRD)

## 1. Overview

**Project Name:** Beauty Treatments Booking Form  
**Version:** 1.0  
**Date:** April 27, 2025  

This document outlines the functional and non-functional requirements for a web-based booking form that allows users to select beauty treatments and add them to a cart for purchase.

## 2. Goals and Success Metrics

- Enable visitors to browse available beauty treatments  
- Allow multi-selection of treatments and add to a shopping cart  
- Display a cart summary with items and total price  
- Provide a seamless, intuitive user experience  

**Success Metrics:**  
- 100% of selected treatments appear in the cart  
- Average page load time under 1 second  
- User error rate below 2% when submitting the form

## 3. User Stories

1. As a visitor, I want to see a list of available treatments with names and prices.
2. As a visitor, I want to select one or more treatments from that list.
3. As a visitor, I want to add selected treatments to a cart.
4. As a visitor, I want to view the cart contents and total cost.
5. As a visitor, I want to return to the booking form to modify my selection.
6. (Future) As a customer, I want to proceed to payment to complete my booking.

## 4. Functional Requirements

- **FR1:** Display treatments retrieved from an in-memory model.  
- **FR2:** Use a multi-select form element (Flask-WTF) for treatment selection.  
- **FR3:** Store selected treatment IDs in user session.  
- **FR4:** Render a cart page listing each treatment and its price.  
- **FR5:** Calculate and display the total price in the cart.  
- **FR6:** Provide navigation between the booking form and cart page.

## 5. Non-Functional Requirements

- **NFR1:** Application must run on Python 3.x with Flask framework.  
- **NFR2:** Templates built using Jinja2.  
- **NFR3:** Secure session handling with a secret key.  
- **NFR4:** Application should be responsive and accessible (WCAG 2.1 AA).  
- **NFR5:** Code organized in MVC-like structure (models, forms, templates).

## 6. Technical Stack

- Language: Python 3.12+  
- Web Framework: Flask  
- Form Library: Flask-WTF (WTForms)  
- Templating: Jinja2  
- Session Management: Flask sessions (server-side cookie)

## 7. Wireframes (High-Level)

1. **Booking Page (/)**
   - Title: "Book Beauty Treatments"
   - Multi-select box listing treatments with price labels
   - "Add to Cart" button

2. **Cart Page (/cart)**
   - Title: "Your Cart"
   - Bullet list of selected treatment names and prices
   - Display of total price
   - Link/button: "Continue Booking"

## 8. Future Enhancements

- Persist data to a database (SQLite, PostgreSQL).  
- User authentication and order history.  
- Payment integration (Stripe, PayPal).  
- Email confirmation and notifications.  
- Admin interface to manage treatments and pricing.

---
*End of PRD*