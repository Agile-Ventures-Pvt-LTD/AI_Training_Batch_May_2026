# M-11: API Documentation

Comprehensive API documentation for Sleepsia Commerce Intelligence Platform

---

## Quick Start

### Authentication

All API requests require a session token:

```bash
curl -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  https://api.sleepsia.com/api/kpis
```

### Base URL

```
https://api.sleepsia.com/api
```

---

## Endpoints

### 1. Upload Dataset

**Upload sales and business data for analysis.**

```
POST /upload
```

#### Request

```bash
curl -X POST https://api.sleepsia.com/api/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@data.xlsx"
```

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | XLSX or XLS file (max 100MB) |

#### Response

```json
{
  "status": "success",
  "dataset_id": "ds_1234567890",
  "metadata": {
    "total_orders": 1500,
    "total_skus": 245,
    "date_range": {
      "start": "2026-01-01",
      "end": "2026-08-30"
    }
  }
}
```

#### Error Responses

- **400 Bad Request**: Invalid file type or too large
- **413 Payload Too Large**: File exceeds 100MB limit
- **500 Internal Error**: Upload processing failed

---

### 2. Calculate KPIs

**Calculate Key Performance Indicators from dataset.**

```
POST /kpis/calculate
```

#### Request

```bash
curl -X POST https://api.sleepsia.com/api/kpis/calculate \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "ds_1234567890",
    "filters": {
      "channel": "Amazon",
      "date": "2026-08-30"
    }
  }'
```

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| dataset_id | String | Yes | Dataset ID from upload |
| filters | Object | No | Filter parameters |
| filters.channel | String | No | Sales channel |
| filters.date | String (YYYY-MM-DD) | No | Single date |
| filters.start_date | String (YYYY-MM-DD) | No | Range start |
| filters.end_date | String (YYYY-MM-DD) | No | Range end |
| filters.sku | String | No | Product SKU |

#### Response

```json
{
  "status": "success",
  "data": {
    "sales": {
      "totalRevenue": 45000.00,
      "netRevenue": 40500.00,
      "unitsSold": 150,
      "aov": 300.00,
      "returnRate": 2.5,
      "cancellationRate": 1.2
    },
    "profitability": {
      "margin": 0.28,
      "marginClass": "excellent",
      "totalProfit": 11340.00
    },
    "advertising": {
      "totalSpend": 5000.00,
      "ctr": 2.5,
      "cpc": 1.25,
      "roas": 8.0
    },
    "shipping": {
      "onTimeDeliveryRate": 96.5,
      "delayedOrders": 5
    }
  }
}
```

#### Error Responses

- **404 Not Found**: Dataset not found
- **400 Bad Request**: Invalid filters
- **500 Internal Error**: KPI calculation failed

---

### 3. Get Insights

**Get AI-generated insights for dataset.**

```
POST /insights/generate
```

#### Request

```bash
curl -X POST https://api.sleepsia.com/api/insights/generate \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "ds_1234567890",
    "focus_area": "profitability"
  }'
```

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| dataset_id | String | Yes | Dataset ID |
| focus_area | String | No | Analysis area (sales, profitability, inventory, shipping) |

#### Response

```json
{
  "status": "success",
  "insights": [
    {
      "type": "opportunity",
      "title": "High-Margin Products",
      "description": "SKU-001 has 35% margin, 10% above average",
      "impact": "high",
      "recommendation": "Increase marketing spend on SKU-001"
    },
    {
      "type": "warning",
      "title": "Shipping Delay Risk",
      "description": "5 orders delayed, affecting customer satisfaction",
      "impact": "medium",
      "recommendation": "Review shipping carrier performance"
    }
  ]
}
```

---

### 4. Compare Competitors

**Get competitor intelligence and pricing analysis.**

```
GET /competitors/analyze
```

#### Request

```bash
curl https://api.sleepsia.com/api/competitors/analyze?dataset_id=ds_123 \
  -H "Authorization: Bearer TOKEN"
```

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| dataset_id | String | Yes | Dataset ID |
| category | String | No | Product category |

#### Response

```json
{
  "status": "success",
  "competitors": [
    {
      "competitor": "BrandX",
      "product": "Competitor Product A",
      "our_sku": "SKU-001",
      "our_price": 499.00,
      "competitor_price": 449.00,
      "price_difference": -50.00,
      "threat_level": "high",
      "promotion": "Summer Sale - 10% off"
    }
  ]
}
```

---

### 5. Health Check

**Check API health status.**

```
GET /health
```

#### Response

```json
{
  "status": "ok",
  "uptime_seconds": 86400,
  "database": "healthy",
  "api": "healthy",
  "cache": "healthy"
}
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| INVALID_FILE_TYPE | 400 | File must be XLSX or XLS |
| FILE_TOO_LARGE | 413 | File exceeds 100MB limit |
| FILE_EMPTY | 400 | File contains no data |
| INVALID_DATE_RANGE | 400 | Date range is invalid |
| MISSING_REQUIRED_FIELD | 400 | Required field is missing |
| DB_CONNECTION_ERROR | 500 | Database connection failed |
| QUERY_TIMEOUT | 500 | Query took too long |
| API_TIMEOUT | 500 | External API timeout |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INVALID_API_KEY | 401 | Invalid authentication |
| SESSION_EXPIRED | 401 | Session has expired |
| NOT_FOUND | 404 | Resource not found |
| INTERNAL_ERROR | 500 | Unexpected error occurred |

---

## Rate Limits

- **Anonymous**: 10 requests/minute
- **User**: 100 requests/minute
- **Premium**: Unlimited

Reset: Limits reset at the start of each minute.

---

## Authentication

### OAuth 2.0 Flow

1. **Redirect to login:**
```
https://api.sleepsia.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI
```

2. **User logs in and grants permission**

3. **Receive authorization code**

4. **Exchange code for token:**
```bash
curl -X POST https://api.sleepsia.com/oauth/token \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

5. **Use token for API requests:**
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.sleepsia.com/api/kpis
```

### Token Refresh

```bash
curl -X POST https://api.sleepsia.com/oauth/token \
  -d "grant_type=refresh_token&refresh_token=REFRESH_TOKEN&client_id=YOUR_CLIENT_ID"
```

---

## Examples

### Python

```python
import requests

API_URL = "https://api.sleepsia.com/api"
TOKEN = "your_session_token"

# Upload file
with open('data.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        f"{API_URL}/upload",
        headers={"Authorization": f"Bearer {TOKEN}"},
        files=files
    )
    dataset_id = response.json()['dataset_id']

# Calculate KPIs
kpi_response = requests.post(
    f"{API_URL}/kpis/calculate",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={
        "dataset_id": dataset_id,
        "filters": {"channel": "Amazon"}
    }
)
kpis = kpi_response.json()['data']
print(f"Total Revenue: ${kpis['sales']['totalRevenue']}")
```

### JavaScript

```javascript
const API_URL = "https://api.sleepsia.com/api";
const TOKEN = "your_session_token";

// Upload file
async function uploadDataset(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    headers: {'Authorization': `Bearer ${TOKEN}`},
    body: formData
  });
  
  return response.json();
}

// Calculate KPIs
async function calculateKPIs(datasetId) {
  const response = await fetch(`${API_URL}/kpis/calculate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      dataset_id: datasetId,
      filters: { channel: 'Amazon' }
    })
  });
  
  return response.json();
}
```

---

## Support

- **Email**: api-support@sleepsia.com
- **Slack**: #api-support channel
- **Documentation**: https://docs.sleepsia.com
- **Status Page**: https://status.sleepsia.com
