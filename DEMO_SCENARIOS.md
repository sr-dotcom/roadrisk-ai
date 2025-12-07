# Demo Test Scenarios - RoadRisk AI

Use these scenarios to demonstrate **Green**, **Yellow**, and **Red** risk predictions.

> **Note:** Weather is fetched LIVE, so predictions vary slightly. Use **Time Override** as your main control.

---

## 🟢 Scenario 1: LOW RISK (Green)

| Setting | Value |
|---------|-------|
| **State** | NC |
| **Address** | 100 N Tryon St, Charlotte |
| **Vehicle Type** | Automobile |
| **Gender** | Male or Female |
| **Time Setting** | Toggle OFF "Use current time" → Select **Morning** |

**Expected Result:** ~1-15% probability

---

## 🟡 Scenario 2: MODERATE RISK (Yellow)

| Setting | Value |
|---------|-------|
| **State** | NY |
| **Address** | Times Square, New York |
| **Vehicle Type** | Heavy Duty Truck |
| **Gender** | Male |
| **Time Setting** | Toggle OFF "Use current time" → Select **Evening** |

**Expected Result:** ~25-45% probability

---

## 🔴 Scenario 3: HIGH RISK (Red)

| Setting | Value |
|---------|-------|
| **State** | FL |
| **Address** | Miami Beach, FL |
| **Vehicle Type** | Heavy Duty Truck |
| **Gender** | Male |
| **Time Setting** | Toggle OFF "Use current time" → Select **Night** |

**Expected Result:** ~50%+ probability

---

## Quick Demo Script

1. **Green**: "Low-risk scenario - standard car in Charlotte during morning hours..."
2. **Yellow**: "Moderate risk - heavy truck in NYC during evening rush..."
3. **Red**: "High-risk - nighttime driving in Florida with a heavy truck..."

---

## Tips

- **Time Override is key** - Toggle OFF "Use current time" to control Morning/Evening/Night
- Night + Heavy Truck = highest risk
- Morning + Automobile = lowest risk
