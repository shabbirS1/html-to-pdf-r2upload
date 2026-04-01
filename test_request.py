import requests
import json

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Receipt</title>
    <style>
        * { box-sizing: border-box !important; padding: 0 !important; }
        body { font-family: 'Courier New', monospace !important; font-size: 12px !important; line-height: 1.2 !important; color: #333 !important; background: #fff !important; width: 320px !important; margin: 0 auto !important; padding: 10px 0 !important; }
        .receipt-container { width: 100% !important; max-width: 320px !important; margin: 0 auto !important; padding: 20px !important; border-radius: 12px !important; box-shadow: 0 5px 20px rgba(0,0,0,0.08) !important; border: 1px solid #e8ecef !important; background: #ffffff !important; }
        .header-section { text-align: center !important; margin-bottom: 5px !important; padding-bottom: 5px !important; border-bottom: 2px solid #f0f3f5 !important; }
        .brand-name { font-size: 24px !important; font-weight: 700 !important; margin-bottom: 5px !important; color: #1a1a1a !important; }
        .info-section { margin-bottom: 18px !important; padding: 12px !important; background: #f8fafc !important; border-radius: 8px !important; }
        .info-item { display: flex !important; justify-content: space-between !important; margin-bottom: 6px !important; font-size: 11px !important; }
        .table-container { margin-bottom: 18px !important; }
        .table-title { font-size: 14px !important; font-weight: 600 !important; margin-bottom: 10px !important; text-align: center !important; padding: 8px !important; background: #f8fafc !important; border-radius: 6px !important; }
        .table { width: 100% !important; border-collapse: collapse !important; font-size: 11px !important; }
        .table th { font-weight: 600 !important; color: #6b7280 !important; text-align: left !important; padding: 8px 6px !important; border-bottom: 2px solid #e8ecef !important; }
        .table td { padding: 8px 6px !important; border-bottom: 1px solid #f0f3f5 !important; }
        .summary-section, .delivery-fee-section, .grand-total-section { margin-bottom: 18px !important; padding: 12px !important; background: #f8fafc !important; border-radius: 8px !important; }
        .summary-title { font-size: 14px !important; font-weight: 600 !important; margin-bottom: 12px !important; text-align: center !important; }
        .summary-item, .delivery-fee-item, .grand-total-item { display: flex !important; justify-content: space-between !important; margin-bottom: 6px !important; font-size: 11px !important; }
        .notes-section, .delivered-by-section { text-align: left !important; margin-top: 20px !important; margin-bottom: 10px !important; padding: 12px !important; background: #f8fafc !important; border-radius: 8px !important; border: 2px solid #e8ecef !important; }
        .notes-text, .delivered-by-text { font-weight: 700 !important; font-size: 13px !important; }
        .bold-text { font-weight: bold; }
        .qr-section { text-align: center !important; margin-top: 18px !important; padding-top: 15px !important; border-top: 2px solid #f0f3f5 !important; }
    </style>
</head>
<body>
    <div class="receipt-container">
        <div class="header-section">
            <div class="brand-name">Burger King</div>
        </div>
        <div class="info-section">
            <div class="info-item bold-text" style="font-size: 16px !important;">
                <span>Order ID: </span><span>77912236</span>
            </div>
            <div class="info-item">
                <span>Order Date: </span><span>01-Mar-2026 10:03:23 AM</span>
            </div>
            <div class="info-item">
                <span>Customer Name: </span><span>فاطمه - السليماني</span>
            </div>
            <div class="info-item">
                <span>Customer Phone: </span><span>50137734</span>
            </div>
        </div>
        <div class="table-container">
            <h3 class="table-title">Order Items</h3>
            <table class="table">
                <thead><tr><th>Item</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr></thead>
                <tbody>
                    <tr><td>MAYO SACHET</td><td>1</td><td>0.050 KWD</td><td>0.050 KWD</td></tr>
                    <tr><td>FREE COKE PET</td><td>1</td><td>0.000 KWD</td><td>0.000 KWD</td></tr>
                    <tr><td>MEGA FRIES ML</td><td>1</td><td>0.000 KWD</td><td>0.000 KWD</td></tr>
                    <tr><td>CHICKEN ROYAL</td><td>1</td><td>0.000 KWD</td><td>0.000 KWD</td></tr>
                    <tr><td>Kids Meal + Mix</td><td>1</td><td>3.500 KWD</td><td>3.500 KWD</td></tr>
                </tbody>
            </table>
        </div>
        <div class="summary-section">
            <h3 class="summary-title">Order Summary</h3>
            <div class="summary-item bold-text"><span>Sub-total: </span><span>3.700 KWD</span></div>
        </div>
        <div class="delivered-by-section">
            <div class="delivered-by-text">Speedy Bunny Delivery Co</div>
        </div>
        <div class="delivery-fee-section">
            <div class="delivery-fee-item bold-text"><span>Delivery Fee: </span><span>0.850 KWD</span></div>
        </div>
        <div class="grand-total-section">
            <div class="grand-total-item bold-text"><span>Grand Total: </span><span>4.550 KWD</span></div>
            <div class="grand-total-item bold-text"><span>Paid Amount: </span><span>-4.550 KWD</span></div>
            <div class="grand-total-item bold-text"><span>Due Amount: </span><span>0.000 KWD</span></div>
        </div>
        <div class="notes-section">
            <div class="notes-text">Thank you for ordering from Burger King</div>
        </div>
    </div>
</body>
</html>'''

payload = {
    "html": html,
    "path": "Media/3/7/Receipt",
    "bucket": "-whatsapp"
}

resp = requests.post("http://100.31.149.135:8001/html-to-pdf-r2", json=payload)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")
