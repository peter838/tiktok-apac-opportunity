# TikTok APAC Opportunity Dashboard

A regional opportunity intelligence dashboard for TikTok APAC markets.

## Overview

This dashboard provides opportunity analysis across 10 APAC markets:
- Singapore (SG)
- China (CN)
- Japan (JP)
- Australia (AU)
- Malaysia (MY)
- Indonesia (ID)
- India (IN)
- Thailand (TH)
- Hong Kong (HK)
- Vietnam (VN)

## Live Deployment

The dashboard is deployed at:
https://tiktok-apac-opportunity.vercel.app

## Structure

- `index.html` - Main regional overview page (TikTok APAC)
- `sg/`, `cn/`, `jp/`, etc. - Individual country pages
- `shared.js` - Shared utilities and data
- `styles.css` - Common styles
- `api/` - API proxy endpoints

## Data Sources

The dashboard pulls live data from the SourceSage API, displaying:
- Actual spend by region
- PO counts
- Cost savings
- Category breakdowns
- Opportunity metrics

---

*Built with the SourceSage Opportunity Intelligence platform*
