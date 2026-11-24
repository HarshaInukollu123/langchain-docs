"""ShopDesk: the make-believe online store used as the story in every lesson.
 
Anyone can follow it: a shopper writes in about an order, ShopDesk helps.
Each day adds one new skill to ShopDesk. This file grows as the story does.
"""
 
SHOP_NAME = "ShopDesk"
 
# Day 01: the very first customer message.
CUSTOMER_MESSAGE = (
    "Hi! I ordered a pair of running shoes last week (order #1042) and it "
    "still hasn't arrived. Can you tell me where it is?"
)
 
# Day 02: ShopDesk's standing instructions (the "system" message) ...
SYSTEM_PROMPT = (
    f"You are {SHOP_NAME}, a friendly support agent for an online store. "
    "Reply in at most 3 sentences. Right now you cannot look up orders or "
    "change anything, so never promise to check or fix something. Instead, "
    "say what you can do and ask the customer for any details you need."
)
 
# ... and the customer's follow-up. "it" only makes sense if you remember
# the first message, which is the whole point of the lesson.
FOLLOW_UP_MESSAGE = "Thanks. Could you send it to my office address instead?"   

ORDERS = {
    "1042": {
        "item": "Trail Runner running shoes",
        "status": "In transit",
        "detail": "Shipped with SwiftShip, delayed at the regional hub. "
        "Expected within 2 business days.",
    },
    "1043": {
        "item": "Wool hiking socks (2-pack)",
        "status": "Delivered",
        "detail": "Left at the front door yesterday.",
    },
}
 
STOCK = {
    "trail runner running shoes": 14,
    "wool hiking socks": 0,
}
 
# Same ShopDesk, but now it is allowed (and expected) to use its tools.
TOOLS_SYSTEM_PROMPT = (
    f"You are {SHOP_NAME}, a friendly support agent for an online store. "
    "Reply in at most 3 sentences. You have tools to look up orders and to "
    "check stock. Use them whenever the customer asks about an order or a "
    "product, and base your answer only on what the tools return."
)
 
# A message that needs no tool at all.
THANKS_MESSAGE = "Thanks, that's all I needed!"