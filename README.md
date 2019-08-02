# Netbill Transaction Protocol Simulator

**What is NetBill?**

NetBill is a system for micropayments for information
goods (digital commodities) on the Internet.
A customer, represented by a client computer, 
wishes to buy information from a merchant’s
server. An account server (the NetBill server), maintains
accounts for both customers and merchants, linked to
conventional financial institutions. A NetBill transaction
transfers information goods from merchant to customer,
debiting the customer’s NetBill account and crediting
the merchant’s account for the value of the goods. When
necessary, funds in a customer’s NetBill account can be
replenished from a bank or credit card; similarly, funds
in a merchant’s NetBill account are made available by
depositing them in the merchant’s bank account.

NetBill requires an efficient set of protocols to
support price negotiation, goods delivery and payment.

**The NetBill Transaction Model**

The NetBill transaction model involves three parties:
the customer, the merchant and the NetBill transaction
server. A transaction involves three phases: price
negotiation, goods delivery, and payment.

![NetBill Transaction Model](https://ai2-s2-public.s3.amazonaws.com/figures/2017-08-08/447c10270e6e3ceac04171c3cb49bd6fdd316ea5/2-Figure1-1.png)
