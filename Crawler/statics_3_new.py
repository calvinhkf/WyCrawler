import os
import database
from draw import draw_bar, draw_barh, draw_line
from file_util import read_json, write_json

db = database.connectdb()

projects = [2, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 20, 21, 22, 23, 24, 28, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 49, 50, 52, 53, 56, 60, 62, 63, 66, 68, 69, 70, 73, 78, 79, 80, 83, 84, 85, 86, 87, 93, 95, 96, 99, 102, 108, 111, 113, 115, 116, 118, 119, 123, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 142, 143, 145, 147, 148, 149, 151, 152, 155, 157, 160, 163, 164, 165, 166, 169, 171, 172, 173, 174, 175, 176, 177, 178, 180, 184, 186, 188, 189, 190, 192, 193, 195, 197, 198, 200, 205, 207, 208, 209, 213, 216, 217, 218, 220, 221, 223, 225, 234, 235, 236, 240, 242, 245, 258, 259, 260, 261, 262, 264, 268, 269, 270, 271, 275, 277, 279, 282, 284, 288, 293, 294, 295, 297, 302, 305, 308, 310, 311, 318, 319, 322, 323, 328, 332, 338, 341, 342, 343, 346, 347, 349, 350, 351, 352, 357, 358, 359, 360, 361, 363, 365, 368, 369, 370, 371, 372, 376, 380, 381, 383, 384, 386, 388, 389, 395, 400, 404, 407, 410, 412, 413, 414, 421, 430, 432, 434, 438, 439, 443, 446, 447, 448, 449, 450, 451, 452, 454, 460, 464, 465, 468, 477, 478, 481, 482, 486, 487, 490, 492, 493, 499, 501, 502, 504, 505, 506, 508, 521, 525, 526, 532, 534, 536, 538, 541, 542, 543, 547, 552, 556, 562, 565, 566, 567, 572, 584, 588, 591, 596, 598, 599, 602, 610, 612, 613, 623, 633, 638, 649, 650, 654, 660, 663, 666, 668, 672, 678, 681, 686, 692, 696, 698, 699, 700, 707, 709, 711, 716, 734, 736, 741, 746, 751, 759, 765, 771, 784, 797, 800, 802, 803, 810, 815, 816, 818, 834, 836, 838, 840, 850, 851, 853, 860, 865, 920, 921, 927, 937, 941, 953, 956, 957, 964, 966, 970, 988, 1006, 1011, 1015, 1022, 1023, 1026, 1028, 1040, 1047, 1056, 1071, 1098, 1103, 1105, 1107, 1109, 1114, 1116, 1120, 1136, 1137, 1139, 1147, 1148, 1154, 1156, 1157, 1170, 1179, 1198, 1201, 1202, 1207, 1213, 1226, 1236, 1237, 1238, 1239, 1240, 1261, 1265, 1269, 1286, 1304, 1306, 1317, 1325, 1342, 1344, 1356, 1358, 1362, 1367, 1370, 1374, 1383, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1396, 1399, 1400, 1401, 1403, 1404, 1406, 1407, 1409, 1412, 1414, 1416, 1417, 1418, 1419, 1421, 1423, 1427, 1428, 1430, 1434, 1435, 1439, 1441, 1442, 1444, 1447, 1450, 1452, 1458, 1460, 1461, 1462, 1464, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1474, 1476, 1481, 1484, 1489, 1490, 1491, 1492, 1493, 1494, 1498, 1501, 1502, 1504, 1505, 1506, 1508, 1510, 1511, 1513, 1515, 1516, 1517, 1520, 1521, 1522, 1526, 1527, 1528, 1529, 1530, 1532, 1534, 1538, 1540, 1541, 1542, 1544, 1546, 1547, 1548, 1552, 1554, 1555, 1556, 1557, 1558, 1565, 1570, 1571, 1573, 1574, 1575, 1578, 1579, 1581, 1582, 1585, 1588, 1590, 1592, 1593, 1594, 1596, 1598, 1599, 1602, 1604, 1608, 1610, 1612, 1618, 1619, 1623, 1627, 1630, 1631, 1633, 1634, 1635, 1639, 1640, 1641, 1653, 1655, 1658, 1659, 1663, 1665, 1669, 1670, 1673, 1674, 1676, 1677, 1678, 1679, 1682, 1686, 1689, 1691, 1692, 1693, 1697, 1698, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1710, 1711, 1713, 1716, 1718, 1722, 1723, 1727, 1730, 1733, 1738, 1749, 1752, 1753, 1754, 1755, 1757, 1758, 1764, 1765, 1767, 1768, 1770, 1772, 1773, 1776, 1778, 1779, 1780, 1784, 1786, 1787, 1792, 1793, 1798, 1799, 1800, 1801, 1806, 1807, 1808, 1809, 1814, 1815, 1819, 1825, 1826, 1834, 1835, 1837, 1839, 1840, 1843, 1852, 1856, 1858, 1860, 1865, 1866, 1867, 1868, 1873, 1874, 1877, 1878, 1879, 1886, 1888, 1893, 1895, 1901, 1903, 1906, 1907, 1909, 1910, 1914, 1919, 1920, 1923, 1925, 1926, 1928, 1929, 1931, 1934, 1939, 1942, 1944, 1948, 1951, 1953, 1954, 1959, 1963, 1964, 1965, 1971, 1980, 1981, 1982, 1992, 1993, 1996, 2004, 2009, 2014, 2016, 2018, 2025, 2028, 2030, 2041, 2048, 2055, 2056, 2057, 2059, 2061, 2064, 2065, 2066, 2067, 2075, 2077, 2081, 2086, 2087, 2089, 2092, 2100, 2110, 2111, 2112, 2116, 2123, 2128, 2130, 2136, 2137, 2172, 2178, 2183, 2200, 2201, 2204, 2208, 2209, 2228, 2230, 2247, 2272, 2274, 2304, 2307, 2318, 2324, 2325, 2336, 2345, 2353, 2366, 2386, 2387, 2391, 2395, 2396, 2398, 2400, 2404, 2405, 2408, 2410, 2413, 2423, 2430, 2433, 2434, 2448, 2450, 2453, 2470, 2471, 2489, 2493, 2512, 2520, 2528, 2544, 2550, 2558, 2566, 2574, 2576, 2580, 2590, 2594, 2598, 2606, 2607, 2608, 2609, 2611, 2628, 2633, 2635, 2638, 2639, 2659, 2660, 2661, 2663, 2665, 2667, 2669, 2673, 2678, 2679, 2682, 2690, 2695, 2696, 2703, 2712, 2713, 2714, 2716, 2721, 2723, 2725, 2731, 2733, 2735, 2737, 2747, 2749, 2757, 2761, 2763, 2769, 2781, 2784, 2785, 2792, 2794, 2796, 2798, 2800, 2802, 2808, 2814, 2816, 2822, 2826, 2834, 2836, 2841, 2843, 2845, 2847, 2852, 2854, 2855, 2857, 2861, 2867, 2871, 2880, 2881, 2883, 2884, 2886, 2890, 2893, 2895, 2896, 2900, 2902, 2909, 2913, 2917, 2918, 2920, 2921, 2923, 2926, 2928, 2929, 2933, 2937, 2939, 2942, 2944, 2946, 2951, 2953, 2955, 2957, 2959, 2965, 2967, 2969, 2971, 2973, 2975, 2979, 2980, 2982, 2983, 2985, 2987, 2989, 2993, 2995, 2997, 2999, 3005, 3007, 3016, 3020, 3024, 3028, 3030, 3036, 3038, 3042, 3044, 3046, 3051, 3053, 3059, 3060, 3062, 3066, 3068, 3070, 3075, 3079, 3081, 3082, 3086, 3088, 3103, 3105, 3106, 3108, 3110, 3115, 3119, 3120, 3124, 3126, 3128, 3129, 3131, 3133, 3146, 3149, 3155, 3158, 3160, 3162, 3168, 3176, 3182, 3186, 3193, 3197, 3202, 3204, 3212, 3214, 3220, 3221, 3225, 3226, 3228, 3230, 3232, 3234, 3236, 3238, 3242, 3244, 3248, 3258, 3266, 3272, 3277, 3281, 3283, 3291, 3293, 3299, 3301, 3303, 3305, 3307, 3315, 3321, 3323, 3325, 3327, 3329, 3333, 3336, 3340, 3344, 3350, 3352, 3355, 3359, 3361, 3363, 3365, 3367, 3369, 3370, 3372, 3374, 3380, 3388, 3398, 3404, 3406, 3411, 3417, 3422, 3424, 3434, 3436, 3437, 3439, 3441, 3445, 3449, 3461, 3465, 3467, 3469, 3475, 3483, 3486, 3488, 3490, 3496, 3498, 3499, 3501, 3505, 3507, 3512, 3516, 3518, 3522, 3524, 3526, 3528, 3533, 3537, 3538, 3544, 3550, 3554, 3555, 3568, 3574, 3576, 3584, 3586, 3588, 3590, 3594, 3597, 3599, 3600, 3606, 3607, 3609, 3615, 3625, 3627, 3629, 3631, 3637, 3640, 3642, 3648, 3657, 3660, 3664, 3671, 3673, 3683, 3687, 3693, 3697, 3709, 3717, 3721, 3729, 3731, 3733, 3737, 3739, 3741, 3743, 3747, 3755, 3757, 3778, 3782, 3784, 3788, 3796, 3798, 3814, 3822, 3828, 3834, 3837, 3847, 3852, 3879, 3887, 3889, 3893, 3903, 3909, 3915, 3922, 3924, 3928, 3932, 3934, 3936, 3941, 3945, 3955, 3964, 3966, 3970, 3974, 4002, 4006, 4008, 4012, 4014, 4015, 4021, 4025, 4030, 4034, 4038, 4041, 4043, 4049, 4054, 4069, 4075, 4087, 4104, 4114, 4124, 4126, 4132, 4140, 4151, 4153, 4161, 4165, 4174, 4178, 4191, 4202, 4210, 4212, 4216, 4227, 4231, 4233, 4234, 4235, 4237, 4239, 4241, 4247, 4255, 4257, 4261, 4267, 4274, 4278, 4284, 4288, 4294, 4306, 4315, 4321, 4323, 4330, 4334, 4343, 4352, 4380, 4388, 4408, 4410, 4414, 4416, 4423, 4447, 4461, 4469, 4473, 4475, 4481, 4485, 4487, 4491, 4493, 4500, 4512, 4514, 4516, 4518, 4524, 4535, 4564, 4574, 4594, 4598, 4600, 4605, 4618, 4638, 4662, 4672, 4674, 4676, 4678, 4695, 4725, 4742, 4744, 4746, 4748, 4754, 4760, 4770, 4774, 4795, 4803, 4811, 4826, 4832, 4846, 4848, 4859, 4865, 4873, 4879, 4883, 4933, 4939, 4941, 4949, 4951, 4957, 4973, 4983, 5005, 5017, 5027, 5033, 5042, 5075, 5079, 5087, 5089, 5096, 5128, 5145, 5153, 5156, 5163, 5165, 5172, 5185, 5214, 5233, 5234, 5236, 5245, 5253, 5260, 5261, 5270, 5273, 5293, 5295, 5302, 5320, 5328, 5330, 5333, 5338, 5348, 5368, 5379, 5399, 5401, 5405, 5408, 5412, 5414, 5432, 5434, 5447, 5454, 5456, 5460, 5461, 5463, 5473, 5475, 5479, 5480, 5486, 5488, 5496, 5501, 5502, 5504, 5507, 5525, 5529, 5533, 5535, 5538]
projects1 = [2, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 20, 21, 22, 23, 24, 28, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 49, 50, 52, 53, 56, 60, 62, 63, 66, 68, 69, 70, 73, 78, 79, 80, 83, 84, 85, 86, 87, 93, 95, 96, 99, 102, 108, 111, 113, 115, 116, 118, 119, 123, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 142, 143, 145, 147, 148, 149, 151, 152, 155, 157, 160, 163, 164, 165, 166, 169, 171, 172, 173, 174, 175, 176, 177, 178, 180, 184, 186, 188, 189, 190, 192, 193, 195, 197, 198, 200, 205, 207, 208, 209, 213, 216, 217, 218, 220, 221, 223, 225, 234, 235, 236, 240, 242, 245, 258, 259, 260, 261, 262, 264, 268, 269, 270, 271, 275, 277, 279, 282, 284, 288, 293, 294, 295, 297, 302, 305, 308, 310, 311, 318, 319, 322, 323, 328, 338, 341, 342, 343, 346, 347, 349, 350, 351, 352, 357, 358, 359, 360, 361, 363, 365, 368, 369, 370, 371, 372, 376, 380, 381, 383, 384, 386, 388, 389, 395, 400, 404, 407, 410, 412, 413, 414, 421, 430, 432, 434, 438, 439, 443, 446, 447, 448, 449, 450, 451, 452, 454, 460, 464, 465, 468, 477, 478, 481, 482, 486, 487, 490, 492, 493, 499, 501, 502, 504, 505, 506, 508, 521, 525, 526, 532, 534, 536, 538, 541, 542, 543, 547, 552, 556, 562, 565, 566, 567, 572, 584, 588, 591, 596, 598, 599, 602, 610, 612, 613, 623, 633, 638, 649, 650, 654, 660, 663, 666, 668, 672, 678, 681, 686, 692, 696, 698, 699, 700, 707, 709, 711, 716, 734, 736, 741, 746, 751, 759, 765, 771, 784, 797, 800, 802, 803, 810, 815, 816, 818, 834, 836, 838, 840, 850, 851, 853, 860, 865, 920, 921, 927, 937, 941, 953, 956, 957, 964, 966, 970, 988, 1006, 1011, 1015, 1022, 1023, 1026, 1028, 1040, 1047, 1056, 1071, 1098, 1103, 1105, 1107, 1109, 1114, 1116, 1120, 1136, 1137, 1139, 1147, 1148, 1154, 1156, 1157, 1170, 1179, 1198, 1201, 1202, 1207, 1213, 1226, 1236, 1237, 1238, 1239, 1240, 1261, 1265, 1269, 1286, 1304, 1306, 1317, 1325, 1342, 1344, 1356, 1358, 1362, 1367, 1370, 1374, 1383, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1396, 1399, 1400, 1401, 1403, 1404, 1406, 1407, 1409, 1412, 1414, 1416, 1417, 1418, 1419, 1421, 1423, 1427, 1428, 1430, 1434, 1435, 1439, 1441, 1442, 1444, 1447, 1450, 1452, 1458, 1460, 1461, 1462, 1464, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1474, 1476, 1481, 1484, 1489, 1490, 1491, 1493, 1494, 1498, 1501, 1502, 1504, 1505, 1506, 1508, 1510, 1511, 1513, 1515, 1516, 1517, 1520, 1521, 1522, 1526, 1527, 1528, 1529, 1530, 1532, 1534, 1538, 1540, 1541, 1542, 1544, 1546, 1547, 1548, 1552, 1554, 1555, 1556, 1557, 1558, 1565, 1570, 1571, 1573, 1574, 1575, 1578, 1579, 1581, 1582, 1585, 1588, 1590, 1592, 1593, 1594, 1596, 1598, 1599, 1602, 1604, 1608, 1610, 1612, 1618, 1619, 1623, 1627, 1630, 1631, 1633, 1634, 1635, 1639, 1640, 1641, 1653, 1655, 1658, 1659, 1663, 1665, 1669, 1670, 1673, 1674, 1676, 1677, 1678, 1679, 1682, 1686, 1689, 1691, 1692, 1693, 1697, 1698, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1710, 1711, 1713, 1716, 1718, 1722, 1723, 1727, 1730, 1733, 1738, 1749, 1752, 1753, 1754, 1755, 1757, 1758, 1764, 1765, 1767, 1768, 1770, 1772, 1773, 1776, 1778, 1779, 1780, 1784, 1786, 1787, 1792, 1793, 1798, 1799, 1800, 1801, 1806, 1807, 1808, 1809, 1814, 1815, 1819, 1825, 1826, 1834, 1835, 1837, 1839, 1840, 1843, 1852, 1856, 1858, 1860, 1865, 1866, 1867, 1868, 1873, 1874, 1877, 1878, 1879, 1886, 1888, 1893, 1895, 1901, 1903, 1906, 1907, 1909, 1910, 1914, 1919, 1920, 1923, 1925, 1926, 1928, 1929, 1931, 1934, 1939, 1942, 1944, 1948, 1953, 1954, 1959, 1963, 1964, 1965, 1971, 1980, 1981, 1982, 1992, 1993, 1996, 2004, 2009, 2014, 2016, 2018, 2025, 2028, 2030, 2041, 2048, 2055, 2056, 2057, 2059, 2061, 2064, 2065, 2066, 2067, 2075, 2077, 2081, 2086, 2087, 2089, 2092, 2100, 2110, 2111, 2112, 2116, 2123, 2128, 2130, 2136, 2137, 2172, 2178, 2183, 2200, 2201, 2204, 2208, 2209, 2228, 2230, 2247, 2272, 2274, 2304, 2307, 2318, 2324, 2325, 2336, 2345, 2353, 2366, 2386, 2387, 2391, 2395, 2396, 2398, 2400, 2404, 2405, 2408, 2410, 2413, 2423, 2430, 2433, 2434, 2448, 2450, 2453, 2470, 2471, 2489, 2493, 2512, 2520, 2528, 2544, 2550, 2558, 2566, 2574, 2576, 2580, 2590, 2594, 2598, 2606, 2607, 2608, 2609, 2611, 2628, 2633, 2635, 2638, 2639, 2659, 2660, 2661, 2663, 2665, 2667, 2669, 2673, 2678, 2679, 2682, 2690, 2695, 2696, 2703, 2712, 2713, 2714, 2716, 2721, 2723, 2725, 2731, 2733, 2735, 2737, 2747, 2749, 2757, 2761, 2763, 2769, 2781, 2784, 2785, 2792, 2794, 2796, 2798, 2800, 2802, 2808, 2816, 2822, 2826, 2834, 2836, 2841, 2843, 2845, 2847, 2852, 2854, 2855, 2857, 2861, 2867, 2871, 2880, 2881, 2883, 2884, 2886, 2890, 2893, 2895, 2896, 2900, 2902, 2909, 2913, 2917, 2918, 2920, 2923, 2926, 2928, 2929, 2933, 2937, 2939, 2942, 2944, 2946, 2951, 2953, 2955, 2957, 2959, 2965, 2967, 2969, 2971, 2973, 2975, 2979, 2980, 2982, 2983, 2985, 2987, 2993, 2995, 2997, 2999, 3005, 3007, 3016, 3020, 3024, 3028, 3030, 3036, 3038, 3042, 3044, 3046, 3051, 3053, 3059, 3060, 3062, 3066, 3068, 3070, 3075, 3079, 3081, 3082, 3086, 3088, 3103, 3105, 3106, 3108, 3110, 3115, 3119, 3120, 3124, 3126, 3128, 3131, 3133, 3146, 3149, 3155, 3158, 3160, 3162, 3168, 3176, 3182, 3186, 3193, 3197, 3202, 3204, 3212, 3214, 3220, 3221, 3225, 3226, 3228, 3230, 3232, 3234, 3236, 3238, 3242, 3244, 3248, 3258, 3266, 3272, 3277, 3281, 3283, 3291, 3293, 3299, 3301, 3303, 3305, 3307, 3315, 3321, 3323, 3325, 3327, 3329, 3333, 3336, 3340, 3344, 3350, 3352, 3355, 3359, 3361, 3363, 3365, 3367, 3369, 3370, 3372, 3374, 3380, 3388, 3404, 3406, 3411, 3417, 3422, 3424, 3434, 3436, 3437, 3439, 3441, 3445, 3449, 3461, 3465, 3467, 3469, 3475, 3483, 3486, 3488, 3490, 3496, 3498, 3499, 3501, 3505, 3507, 3512, 3516, 3518, 3522, 3524, 3526, 3528, 3533, 3537, 3538, 3544, 3550, 3554, 3555, 3568, 3574, 3576, 3584, 3586, 3588, 3590, 3594, 3597, 3599, 3600, 3606, 3607, 3609, 3615, 3625, 3627, 3629, 3631, 3637, 3640, 3642, 3648, 3657, 3660, 3664, 3671, 3673, 3683, 3687, 3693, 3697, 3709, 3717, 3721, 3729, 3731, 3733, 3737, 3739, 3741, 3743, 3747, 3755, 3757, 3778, 3782, 3784, 3788, 3796, 3798, 3814, 3822, 3828, 3834, 3837, 3847, 3852, 3879, 3887, 3889, 3893, 3903, 3909, 3915, 3922, 3924, 3928, 3932, 3934, 3936, 3941, 3945, 3955, 3964, 3966, 3970, 3974, 4002, 4006, 4008, 4012, 4014, 4015, 4021, 4025, 4030, 4034, 4038, 4041, 4043, 4049, 4054, 4069, 4075, 4087, 4104, 4114, 4124, 4126, 4132, 4140, 4151, 4153, 4161, 4165, 4174, 4178, 4191, 4202, 4210, 4212, 4216, 4227, 4231, 4233, 4234, 4235, 4237, 4239, 4241, 4247, 4255, 4257, 4261, 4267, 4274, 4278, 4284, 4288, 4294, 4306, 4315, 4321, 4330, 4334, 4343, 4352, 4380, 4388, 4408, 4410, 4414, 4416, 4423, 4447, 4461, 4469, 4473, 4475, 4481, 4485, 4487, 4491, 4493, 4500, 4512, 4514, 4516, 4518, 4524, 4535, 4564, 4574, 4594, 4598, 4600, 4605, 4618, 4638, 4662, 4672, 4674, 4676, 4678, 4695, 4725, 4742, 4744, 4746, 4748, 4754, 4760, 4770, 4774, 4795, 4803, 4811, 4826, 4832, 4846, 4848, 4859, 4865, 4873, 4879, 4883, 4933, 4939, 4941, 4949, 4951, 4957, 4973, 4983, 5005, 5017, 5027, 5033, 5042, 5075, 5079, 5087, 5089, 5096, 5128, 5145, 5153, 5156, 5163, 5165, 5172, 5185, 5214, 5233, 5234, 5236, 5245, 5253, 5260, 5261, 5270, 5273, 5293, 5295, 5302, 5320, 5328, 5330, 5333, 5338, 5348, 5368, 5379, 5399, 5401, 5405, 5408, 5412, 5414, 5432, 5434, 5447, 5454, 5456, 5460, 5461, 5463, 5473, 5475, 5479, 5480, 5486, 5488, 5496, 5501, 5502, 5504, 5507, 5525, 5529, 5533, 5535, 5538]

def project():
    sql = "SELECT DISTINCT project_id FROM `usage`"
    query_result = database.querydb(db, sql)
    ids = []
    for entry in query_result:
        id = entry[0]
        ids.append(id)
    print(ids)
    print(len(ids))

def s_3_1_1():
    usage_count = []
    for id in projects:
        # print(id)
        sql = "SELECT count(DISTINCT group_str,name_str,version) FROM `usage` WHERE project_id = " + str(id)
        usage_info = database.querydb(db, sql)
        usage_count.append(usage_info[0][0])
        if usage_info[0][0] == 1347:
            print(id)
        # usage_count.append(len(usage_info))
        # if len(usage_info) == 732:
        #     print(id)
        # print(str(id)+" "+str(len(usage_info)))
    # usage_count.sort()
    # write_json("D:/data/data_copy/figure/datas/s_3_1_1.txt", usage_count)
    # keys = ['']*25
    # values = [0]*25
    # keys[0] = '0'
    # values[0] = 1329 - 1281
    # for i in range(0,20):
    #     start = i*5
    #     end = i*5 + 5
    #     keys[i+1] = str(start) + "-" + str(end)
    # keys[21] = '100-150'
    # keys[22] = '150-200'
    # keys[23] = '200-250'
    # keys[24] = '>250'
    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_1.txt")
    # print(len(usage_count))
    # count = 0
    # for num in usage_count:
    #     if num > 250:
    #         values[24] += 1
    #     elif num > 200 and num <= 250:
    #         values[23] += 1
    #     elif num > 150 and num <= 200:
    #         values[22] += 1
    #     elif num > 100 and num <= 150:
    #         values[21] += 1
    #     else:
    #         index = num // 5 + 1
    #         if num % 5 == 0:
    #             index -= 1
    #         values[index] += 1
    #
    # draw_bar(keys, values, "The Number of Library Versions Used in a Project (#)", "The Number of Projects (#)")

    # print(usage_count)
    # data_group_unique(usage_count, 10, "the number of library versions used in a project", "the number of projects")

def s_3_1_2():
    # versions = []
    # sql = "SELECT distinct group_str,name_str,version FROM `usage`"
    # query_result = database.querydb(db, sql)
    # versions = list(query_result)
    # print(versions)
    # print(len(versions))
    # write_json("D:/data/data_copy/figure/datas/versions.txt",versions)

    # versions = read_json("D:/data/data_copy/figure/datas/versions.txt")
    # usage_count = []
    # for entry in versions:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     version = entry[2]
    #     sql = "SELECT DISTINCT(project_id) FROM `usage` WHERE group_str = '" +groupId + "' and name_str = '" + artifactId+ "' and version = '" +version + "'"
    #     usage_info = database.querydb(db, sql)
    #     usage_count.append(len(usage_info))
    # write_json("D:/data/data_copy/figure/datas/s_3_1_2.txt", usage_count)

    keys = [''] * 25
    values = [0] * 25
    for i in range(1, 21):
        keys[i - 1] = str(i)
    keys[20] = '20-40'
    keys[21] = '40-60'
    keys[22] = '60-80'
    keys[23] = '80-100'
    keys[24] = '>100'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_2.txt")
    count = 0
    for num in usage_count:
        if num > 100:
            values[24] += 1
        elif num > 80 and num <= 100:
            values[23] += 1
        elif num > 60 and num <= 80:
            values[22] += 1
        elif num > 40 and num <= 60:
            values[21] += 1
        elif num > 20 and num <= 40:
            values[20] += 1
        else:
            values[num-1] += 1
    draw_bar(keys, values, "The Number of Projects Using a Library Version (#)", "The Number of Library Versions (#)")
    # data_group(usage_count, 2, "the number of projects using a library version", "the number of library versions")

def s_3_1_3():
    # libraries = []
    # sql = "SELECT distinct group_str,name_str FROM `usage`"
    # query_result = database.querydb(db, sql)
    # libraries = list(query_result)
    # print(len(libraries))
    # print(libraries)
    # write_json("D:/data/data_copy/figure/datas/libraries.txt", libraries)

    # libraries = read_json("D:/data/data_copy/figure/datas/libraries.txt")
    # usage_count = []
    # for entry in libraries:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     sql = "SELECT DISTINCT(project_id) FROM `usage` WHERE group_str = '" +groupId + "' and name_str = '" + artifactId + "'"
    #     usage_info = database.querydb(db, sql)
    #     usage_count.append(len(usage_info))
    # write_json("D:/data/data_copy/figure/datas/s_3_1_3.txt", usage_count)

    keys = [''] * 25
    values = [0] * 25
    for i in range(1, 21):
        keys[i - 1] = str(i)
    keys[20] = '20-40'
    keys[21] = '40-60'
    keys[22] = '60-80'
    keys[23] = '80-100'
    keys[24] = '>100'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_3.txt")
    count = 0
    for num in usage_count:
        if num > 100:
            values[24] += 1
        elif num > 80 and num <= 100:
            values[23] += 1
        elif num > 60 and num <= 80:
            values[22] += 1
        elif num > 40 and num <= 60:
            values[21] += 1
        elif num > 20 and num <= 40:
            values[20] += 1
        else:
            values[num - 1] += 1
    draw_bar(keys, values, "The Number of Projects Using a Library (#)", "The Number of Libraries (#)")

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_3.txt")
    # data_group(usage_count, 2, "the number of projects using a library", "the number of libraries")

def s_3_1_4_1():
    # usage_count = []
    # for id in projects:
    #     # print(id)
    #     sql = "SELECT DISTINCT group_str,name_str FROM `usage` WHERE project_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     num = 0
    #     for entry in usage_info:
    #         groupId = entry[0]
    #         artifactId = entry[1]
    #         sql = "SELECT COUNT(DISTINCT(version)) FROM `usage` WHERE project_id = " + str(id) + " and group_str = '"+groupId+"' and name_str = '"+artifactId+"'"
    #         result = database.querydb(db, sql)
    #         if result[0][0] > 1:
    #             # if id == 359:
    #             #     print(library_id)
    #                 # print(result[0][0])
    #             num += 1
    #     usage_count.append(num)
    # print(usage_count)
    # write_json("D:/data/data_copy/figure/datas/s_3_1_4.1.txt", usage_count)

    keys = [''] * 26
    values = [0] * 26
    for i in range(0, 21):
        keys[i] = str(i)
    keys[21] = '20-25'
    keys[22] = '25-30'
    keys[23] = '30-35'
    keys[24] = '35-40'
    keys[25] = '>40'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_4.1.txt")
    count = 0
    for num in usage_count:
        if num > 40:
            values[25] += 1
        elif num > 35 and num <= 40:
            values[24] += 1
        elif num > 30 and num <= 35:
            values[23] += 1
        elif num > 25 and num <= 30:
            values[22] += 1
        elif num > 20 and num <= 25:
            values[21] += 1
        else:
            values[num] += 1
    draw_bar(keys, values, "The Number of Libraries Whose Different Versions Are Used in a Project (#)", "The Number of Projects (#)")

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_4.1.txt")
    # data_group(usage_count, 1, "the number of libraries whose different versions are used in a project", "the number of projects", True)

def s_3_1_4_2():
    # usage_count = []
    # for id in projects:
    #     # print(id)
    #     sql = "SELECT DISTINCT group_str,name_str FROM `usage` WHERE project_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     num = 0
    #     for entry in usage_info:
    #         groupId = entry[0]
    #         artifactId = entry[1]
    #         sql = "SELECT COUNT(DISTINCT(version)) FROM `usage` WHERE project_id = " + str(id) + " and group_str = '"+groupId+"' and name_str = '"+artifactId+"'"
    #         result = database.querydb(db, sql)
    #         if result[0][0] > 1:
    #             usage_count.append(result[0][0])
    # print(usage_count)
    # write_json("D:/data/data_copy/figure/datas/s_3_1_4.2.txt", usage_count)

    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_4.2.txt")
    print(len(usage_count))
    data_group(usage_count, 1, "The Number of Used Versions of the Same Library (#)", "The Number of Multi-Version Cases (#)", True)

def s_3_1_5():
    # usage_count = []
    # for id in projects:
    #     # print(id)
    #     sql = "SELECT COUNT(DISTINCT group_str,name_str,version) FROM `usage` WHERE version like '%SNAPSHOT' and project_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     usage_count.append(usage_info[0][0])
    # print(usage_count)
    # write_json("D:/data/data_copy/figure/datas/s_3_1_5.txt", usage_count)

    keys = [''] * 26
    values = [0] * 26
    keys[0] = '0'
    for i in range(0, 20):
        start = i * 5
        end = i * 5 + 5
        keys[i + 1] = str(start) + "-" + str(end)
    keys[21] = '100-150'
    keys[22] = '150-200'
    keys[23] = '200-250'
    keys[24] = '250-300'
    keys[25] = '>300'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_5.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 300:
            values[25] += 1
        elif num > 250 and num <= 300:
            values[24] += 1
        elif num > 200 and num <= 250:
            values[23] += 1
        elif num > 150 and num <= 200:
            values[22] += 1
        elif num > 100 and num <= 150:
            values[21] += 1
        elif num == 0:
            values[0] += 1
        else:
            index = num // 5 + 1
            if num % 5 == 0:
                index -= 1
            values[index] += 1
    draw_bar(keys, values, "The Number of Snapshot Versions in a Project (#)", "The Number of Projects (#)")

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_5.txt")
    # print(len(usage_count))
    # data_group(usage_count, 5, "The Number of Snapshot Versions in a Project", "The Number of Projects", False)

def s_3_1_6():
    # usage_count = {}
    # libraries = read_json("D:/data/data_copy/figure/datas/libraries.txt")
    # for entry in libraries:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     sql = "SELECT DISTINCT(project_id) FROM `usage` WHERE group_str = '" +groupId + "' and name_str = '" + artifactId + "'"
    #     usage_info = database.querydb(db, sql)
    #     name = groupId + " " + artifactId
    #     usage_count[name] = len(usage_info)
    #
    # sorted_usage = sorted(usage_count.items(), key=lambda d: d[1], reverse=True)
    # sorted_usage = sorted_usage[:20]
    # print(sorted_usage)
    #
    # sorted_usage = [('junit junit', 1011), ('org.slf4j slf4j-api', 525), ('com.google.guava guava', 412),
    #                 ('org.mockito mockito-core', 339), ('commons-io commons-io', 335),
    #                 ('com.fasterxml.jackson.core jackson-databind', 302), ('org.apache.commons commons-lang3', 262),
    #                 ('log4j log4j', 257), ('ch.qos.logback logback-classic', 241), ('org.slf4j slf4j-log4j12', 223),
    #                 ('org.apache.httpcomponents httpclient', 217), ('javax.servlet javax.servlet-api', 205),
    #                 ('com.google.code.gson gson', 192), ('commons-lang commons-lang', 185),
    #                 ('commons-codec commons-codec', 182), ('com.fasterxml.jackson.core jackson-core', 178),
    #                 ('org.mockito mockito-all', 177), ('org.springframework spring-test', 177),
    #                 ('joda-time joda-time', 167), ('org.springframework spring-context', 166)]

    sorted_usage = [('JUnit', 1011), ('SLF4J API Module', 525), ('Guava: Google Core Libraries For Java', 412),
                    ('Mockito Core', 339), ('Apache Commons IO', 335), ('Jackson Databind', 302),
                    ('Apache Commons Lang', 262), ('Apache Log4j', 257), ('Logback Classic Module', 241),
                    ('SLF4J LOG4J 12 Binding', 223), ('Apache HttpClient', 217), ('Java Servlet API', 205),
                    ('Gson', 192), ('Commons Lang', 185), ('Apache Commons Codec', 182), ('Jackson Core', 178),
                    ('Mockito', 177), ('Spring TestContext Framework', 177),
                    ('Joda Time', 167), ('Spring Context', 166)]
    sorted_usage = sorted_usage[::-1]
    print(sorted_usage)
    values = [value for key, value in sorted_usage]
    keys = [key for key, value in sorted_usage]

    draw_barh(keys, values)

def s_3_1_7():
    # usage_count = {}
    # sql = "SELECT DISTINCT(version) FROM `usage` WHERE group_str = 'junit' and name_str = 'junit'"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     version = entry[0]
    #     sql = "SELECT COUNT(DISTINCT(project_id)) FROM `usage` WHERE group_str = 'junit' and name_str = 'junit' and version = '" + str(version) + "'"
    #     result = database.querydb(db, sql)
    #     usage_count[version] = result[0][0]
    # print(usage_count)
    # write_json("D:/data/data_copy/figure/datas/s_3_1_7.txt", usage_count)
    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_7.txt")
    # sorted_usage = sorted(usage_count.items(), key=lambda d: d[0])
    # print(sorted_usage)
    usage_count = [('3.8.1', 47), ('3.8.2', 8), ('4.0', 3), ('4.1', 1), ('4.2', 2),
                   ('4.3', 1), ('4.3.1', 1), ('4.4', 11), ('4.5', 11), ('4.6', 4), ('4.7', 15), ('4.8', 7),
                   ('4.8.1', 26), ('4.8.2', 52), ('4.9', 9), ('4.10', 84),('4.10-HBASE-1', 1),
                   ('4.11', 269), ('4.11-beta-1', 0), ('4.12', 599), ('4.12-beta-1', 0), ('4.12-beta-2', 0), ('4.12-beta-3', 1), ('4.12.3', 1), ('4.13-SNAPSHOT', 2)]

    # usage_count = [('3.8.1', 47), ('3.8.2', 8), ('4.0', 2), ('4.1', 1), ('4.2', 2), ('4.3', 1), ('4.3.1', 1), ('4.4', 11), ('4.5', 11),
    #  ('4.6', 4), ('4.7', 15), ('4.8', 7), ('4.8.1', 26), ('4.8.2', 52), ('4.9', 9), ('4.10', 84), ('4.11', 269), ('4.12', 599),
    #  ('4.12-beta-3', 1), ('4.13-SNAPSHOT', 2)]
    new_usage = {}
    for entry in usage_count:
        if entry[1] != 0:
            new_usage[entry[0]] = entry[1]
    new_usage = sorted(new_usage.items(), key=lambda d: d[1], reverse=True)
    new_usage = new_usage[::-1]
    print(new_usage)
    values = [value for key, value in new_usage]
    keys = [key for key, value in new_usage]
    draw_barh(keys, values)
    # draw_bar(keys, values, "JUnit Version", "The Number of Projects (#)")

def data_group(li,step,x_label,y_label, is_single_label):
    li.sort()
    length = li[-1]//step
    if li[-1] % step > 0:
        length += 1
    length = int(round(length, 0))
    label_list = ['']*length
    value_list = [0]*length
    for i in range(length):
        if is_single_label:
            # label_list[i] = str(float(i * step))
            label_list[i] = str(i * step)
        else:
            # label_list[i] = str(float(i * step)) + "-" + str(float((i + 1) * step))
            label_list[i] = str(i * step) + "-" + str((i + 1) * step)
    # label_list[len(label_list)-1] = "24"
    li.sort()
    for num in li:
        index = num // step
        index = int(round(index, 0))
        if index == length:
            index -= 1
        if index < 0:
            print(str(num)+"  "+str(num // step)+"  "+str(int(round(num // step, 0))))
            continue
        value_list[index] += 1

    for i in range(len(value_list) - 1, -1, -1):
        if value_list[i] == 0:
            del value_list[i]
            del label_list[i]
    draw_bar(label_list, value_list, x_label, y_label)
    # return label_list,value_list

def lib_used_api():
    dir = "D:/data/data_copy/RQ1/project_call/api_call/"
    file_list = os.listdir(dir)
    for file in file_list:
        if os.path.exists("D:/data/data_copy/RQ1/project_call/project_percent/" + file):
            continue
        project_id = int(file.replace(".txt", ""))
        # if project_id == 1707:
        #     continue
        print("+++++++++++++++++++++++++++++++" + file)
        json_data = read_json(os.path.join(dir, file))
        callInParent = json_data["callInParent"]
        otherDeclaration = json_data["otherDeclaration"]
        proj_total_count = len(callInParent) + len(otherDeclaration)
        proj_method_count = 0
        lib_apis = {}
        for entry in callInParent:
            call_list = entry["call_list"]
            has_call = 0
            for call_obj in call_list:
                if "lib" in call_obj:
                    has_call += 1
                    lib = call_obj["lib"]
                    call = call_obj["api"]
                    if lib in lib_apis:
                        lib_apis[lib].add(call)
                    else:
                        lib_apis[lib] = set()
                        lib_apis[lib].add(call)
            if has_call > 0:
                proj_method_count += 1

        temp = [proj_total_count, proj_method_count]
        write_json("D:/data/data_copy/RQ1/project_call/project_percent/" + file, temp)
        for lib in lib_apis.keys():
            if os.path.exists("D:/data/data_copy/RQ1/project_call/lib_percent/"+lib+".txt"):
                prev_list = read_json("D:/data/data_copy/RQ1/project_call/lib_percent/"+lib+".txt")
                prev_set = set(prev_list)
                prev_set.union(lib_apis[lib])
                write_json("D:/data/data_copy/RQ1/project_call/lib_percent/"+lib+".txt", list(prev_set))
            else:
                write_json("D:/data/data_copy/RQ1/project_call/lib_percent/" + lib + ".txt", list(lib_apis[lib]))
        # break

def lib_percent():
    dir = "D:/data/data_copy/lib_to_field/preprocessed_api"
    files = os.listdir(dir)
    version_dic = {}
    count = 0
    for file in files:
        jar_name = file.replace(".json", "")
        if not jar_name.endswith(".jar"):
            continue
        print(jar_name)
        sql = "SELECT type_id,version_id FROM version_types WHERE jar_package_url = '" + jar_name + "'"
        query_result = database.querydb(db, sql)
        if len(query_result) <= 0:
            continue
        version_id = str(query_result[0][1])
        api_list = read_json(os.path.join(dir, file))
        if len(api_list) == 0:
            count += 1
            continue
        if os.path.exists("D:/data/data_copy/RQ1/project_call/lib_percent/" + jar_name + ".txt"):
            used_api = read_json("D:/data/data_copy/RQ1/project_call/lib_percent/" + jar_name + ".txt")
            percent = len(used_api) / len(api_list) * 100
        else:
            percent = 0 / len(api_list) * 100
        if version_id in version_dic:
            if percent > version_dic[version_id]:
                version_dic[version_id] = percent
        else:
            version_dic[version_id] = percent
    print(count) #1304
    print(version_dic)
    print(len(version_dic)) #18579

def s_3_2_1():
    # percent_count = []
    # count = 0
    # dir = "D:/data/data_copy/RQ1/project_call/project_percent"
    # files = os.listdir(dir)
    # for file in files:
    #     print("++++++++++++" + file)
    #     counts = read_json(os.path.join(dir, file))
    #     if counts[0] == 0:
    #         print("counts[0] == 0")
    #         count += 1
    #         continue
    #     percent_count.append(counts[1] / counts[0] * 100)
    # percent_count.sort()
    # print(percent_count)
    # print(len(percent_count))
    # print(count)
    # write_json("D:/data/data_copy/figure/datas/s_3_2_1.txt", percent_count)

    # percent_count = read_json("D:/data/data_copy/figure/datas/s_3_2_1.txt")
    # data_group(percent_count, 2, "The Percent of a Project’s Methods That Call Library APIs (%)", "The Number of Projects (#)", False)

    keys = [''] * 30
    values = [0] * 30
    keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i + 1] = str(start) + "-" + str(end)
    keys[26] = '50-60'
    keys[27] = '60-70'
    keys[28] = '70-80'
    keys[29] = '80-90'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_2_1.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 80 and num <= 90:
            values[29] += 1
        elif num > 70 and num <= 80:
            values[28] += 1
        elif num > 60 and num <= 70:
            values[27] += 1
        elif num > 50 and num <= 60:
            values[26] += 1
        elif num == 0:
            values[0] += 1
        else:
            index = num // 2 + 1
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            values[index] += 1
    values[0] += 1329-len(usage_count)
    draw_bar(keys, values, "The Percent of a Project’s Methods That Call Library APIs (%)", "The Number of Projects (#)")

def s_3_2_2():
    # version_dic = read_json("D:/data/data_copy/RQ1/project_call/lib_percent.txt")
    # percent_count = list(version_dic.values())
    # print(len(percent_count))
    # data_group(percent_count, 2, "The Percent of a Library Version’s APIs That Are Called Across Projects (%)", "The Number of Library Versions (#)", False)

    keys = [''] * 30
    values = [0] * 30
    # keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i] = str(start) + "-" + str(end)
    keys[25] = '50-60'
    keys[26] = '60-70'
    keys[27] = '70-80'
    keys[28] = '80-90'
    keys[29] = '90-100'
    percent_count = read_json("D:/data/data_copy/RQ1/project_call/lib_percent.txt")
    usage_count = list(percent_count.values())
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 90 and num <= 100:
            values[29] += 1
        elif num > 80 and num <= 90:
            values[28] += 1
        elif num > 70 and num <= 80:
            values[27] += 1
        elif num > 60 and num <= 70:
            values[26] += 1
        elif num > 50 and num <= 60:
            values[25] += 1
        # elif num == 0:
        #     values[0] += 1
        else:
            index = num // 2
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            if index < 0:
                index = 0
            values[index] += 1
    # draw_bar(keys, values, "The Percent of a Library Version’s APIs That Are Called Across Projects (%)", "The Number of Library Versions (#)")

def s_3_2_3():
    # new_dic = {}
    # version_dic = read_json("D:/data/data_copy/RQ1/project_call/lib_percent.txt")
    # count = 0
    # for version in version_dic.keys():
    #     percent = version_dic[version]
    #     sql = "SELECT library_id FROM project_lib_usage WHERE version_id = " + version
    #     query_result = database.querydb(db, sql)
    #     if len(query_result) <= 0:
    #         count += 1
    #         print(version)
    #         continue
    #     library_id = str(query_result[0][0])
    #     if library_id in new_dic:
    #         if percent > new_dic[library_id]:
    #             new_dic[library_id] = percent
    #     else:
    #         new_dic[library_id] = percent
    #
    # print(count) #750
    # print(new_dic)
    # print(len(new_dic))#7487
    # write_json("D:/data/data_copy/figure/datas/s_3_2_3.txt", list(new_dic.values()))

    # percent_count = read_json("D:/data/data_copy/figure/datas/s_3_2_3.txt")
    # print(len(percent_count))
    # data_group(percent_count, 2, "The Percent of a Library’s APIs That Are Called Across Projects (%)","The Number of Libraries (#)", False)
    keys = [''] * 30
    values = [0] * 30
    # keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i] = str(start) + "-" + str(end)
    keys[25] = '50-60'
    keys[26] = '60-70'
    keys[27] = '70-80'
    keys[28] = '80-90'
    keys[29] = '90-100'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_2_3.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 90 and num <= 100:
            values[29] += 1
        elif num > 80 and num <= 90:
            values[28] += 1
        elif num > 70 and num <= 80:
            values[27] += 1
        elif num > 60 and num <= 70:
            values[26] += 1
        elif num > 50 and num <= 60:
            values[25] += 1
        # elif num == 0:
        #     values[0] += 1
        else:
            index = num // 2
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            if index < 0:
                index = 0
            values[index] += 1
    # draw_bar(keys, values, "The Percent of a Library’s APIs That Are Called Across Projects (%)","The Number of Libraries (#)")

def outdateness():
    # json_data = read_json("E:/data/projs.8.11.time.json")
    # final_result = {}
    # for entry in json_data:
    #     download_time = entry['download_time']
    #     url = entry["url"]
    #     sql = "SELECT * FROM project WHERE url = '" + url + "'"
    #     query_result = database.querydb(db, sql)
    #     project_id = str(query_result[0][0])
    #     final_result[project_id] = download_time
    # print(len(final_result))
    # write_json("E:/data/download_time.json", final_result)

    download_time = read_json("E:/data/download_time.json")
    sql = "SELECT * FROM project_lib_usage"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    for entry in query_result:
        project_id = entry[0]
        type_id = entry[1]
        module = entry[2]
        version_id = entry[4]
        sql = "SELECT group_str,name_str,repository,parsed_date FROM library_versions WHERE id = " + str(version_id)
        version_info = database.querydb(db, sql)
        groupId = version_info[0][0]
        artifactId = version_info[0][1]
        repository = version_info[0][2]
        release_date = version_info[0][3]
        sql = "SELECT count(*) FROM library_versions WHERE group_str = '" + groupId + "' and name_str = '" + artifactId + "' and repository = '" + repository + "' and parsed_date > '" + str(release_date) + "' and parsed_date < '" + download_time[str(project_id)] + "'"
        count_result = database.querydb(db,sql)
        sql = "UPDATE project_lib_usage SET outdate = " + str(count_result[0][0]) + " WHERE project_id = " + str(project_id) + " and version_type_id = " + str(type_id) + " and module = '" + module + "'"
        database.execute_sql(db, sql)
        # break

def s_3_3_1():
    # nine_month = read_json("D:/data/data_copy/figure/datas/three_month.txt")
    # # print(len(nine_month))
    # usage_count = []
    # for id in nine_month:
    #     print(id)
    #     sql = "SELECT outdate FROM project_lib_usage WHERE project_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     if len(usage_info) <= 0:
    #         continue
    #     total = 0
    #     for entry in usage_info:
    #         total += entry[0]
    #     usage_count.append(total/len(usage_info))
    #     print(total/len(usage_info))
    #     break
    # usage_count.sort()
    # print(usage_count)
    # print(len(usage_count))
    # write_json("D:/data/data_copy/figure/datas/s_3_3_1_three.txt", usage_count)

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_1.txt")
    # data_group(usage_count, 2, "The Average Usage Outdatedness of the Library Dependencies in a Project (#)","The Number of Projects (#)", False)

    keys = [''] * 32
    values = [0] * 32
    keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i + 1] = str(start) + "-" + str(end)
    keys[26] = '50-60'
    keys[27] = '60-70'
    keys[28] = '70-80'
    keys[29] = '80-90'
    keys[30] = '90-100'
    keys[31] = '100-300'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_1.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 100 and num <= 300:
            values[31] += 1
        elif num > 90 and num <= 100:
            values[30] += 1
        elif num > 80 and num <= 90:
            values[29] += 1
        elif num > 70 and num <= 80:
            values[28] += 1
        elif num > 60 and num <= 70:
            values[27] += 1
        elif num > 50 and num <= 60:
            values[26] += 1
        elif num == 0:
            values[0] += 1
        else:
            index = num // 2 + 1
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            values[index] += 1
    draw_bar(keys, values, "The Average Usage Outdatedness of the Library Dependencies in a Project (#)", "The Number of Projects (#)")

def s_3_3_2 ():
    # nine_month = read_json("D:/data/data_copy/figure/datas/three_month.txt")
    # versions = read_json("D:/data/data_copy/figure/datas/version_ids.txt")
    # usage_count = []
    # for id in versions:
    #     # print(id)
    #     sql = "SELECT project_id,outdate FROM project_lib_usage WHERE version_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     total = 0
    #     length = 0
    #     for entry in usage_info:
    #         project_id = entry[0]
    #         if project_id in nine_month:
    #             total += entry[1]
    #             length += 1
    #     if length > 0:
    #         usage_count.append(total/length)
    # usage_count.sort()
    # print(usage_count)
    # print(len(usage_count))
    # write_json("D:/data/data_copy/figure/datas/s_3_3_2_three.txt", usage_count)

    # versions = read_json("D:/data/data_copy/figure/datas/version_ids.txt")
    # usage_count = []
    # for id in versions:
    #     # print(id)
    #     sql = "SELECT outdate FROM project_lib_usage WHERE version_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     total = 0
    #     for entry in usage_info:
    #         total += entry[0]
    #     usage_count.append(total/len(usage_info))
    # usage_count.sort()
    # print(usage_count)
    # print(len(usage_count))
    # write_json("D:/data/data_copy/figure/datas/s_3_3_2.txt", usage_count)

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_2.txt")
    # data_group(usage_count, 20, "The Average Usage Outdatedness of the Library Dependencies on a Library Version (#)","The Number of Library Versions (#)", False)
    keys = [''] * 33
    values = [0] * 33
    keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i + 1] = str(start) + "-" + str(end)
    keys[26] = '50-60'
    keys[27] = '60-70'
    keys[28] = '70-80'
    keys[29] = '80-90'
    keys[30] = '90-100'
    keys[31] = '100-300'
    keys[32] = '300-2240'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_2.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 300 and num <= 2240:
            values[32] += 1
        elif num > 100 and num <= 300:
            values[31] += 1
        elif num > 90 and num <= 100:
            values[30] += 1
        elif num > 80 and num <= 90:
            values[29] += 1
        elif num > 70 and num <= 80:
            values[28] += 1
        elif num > 60 and num <= 70:
            values[27] += 1
        elif num > 50 and num <= 60:
            values[26] += 1
        elif num == 0:
            values[0] += 1
        else:
            index = num // 2 + 1
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            values[index] += 1
    # draw_bar(keys, values, "The Average Usage Outdatedness of the Library Dependencies on a Library Version (#)","The Number of Library Versions (#)")

def s_3_3_3 ():
    # nine_month = read_json("D:/data/data_copy/figure/datas/three_month.txt")
    # libraries = read_json("D:/data/data_copy/figure/datas/library_ids.txt")
    # usage_count = []
    # for id in libraries:
    #     sql = "SELECT project_id,outdate FROM project_lib_usage WHERE library_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     total = 0
    #     length = 0
    #     for entry in usage_info:
    #         project_id = entry[0]
    #         if project_id in nine_month:
    #             total += entry[1]
    #             length += 1
    #     if length > 0:
    #         usage_count.append(total/length)
    # usage_count.sort()
    # print(usage_count)
    # print(len(usage_count))
    # write_json("D:/data/data_copy/figure/datas/s_3_3_3_three.txt", usage_count)

    # libraries = read_json("D:/data/data_copy/figure/datas/library_ids.txt")
    # usage_count = []
    # for id in libraries:
    #     sql = "SELECT outdate FROM project_lib_usage WHERE library_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     total = 0
    #     for entry in usage_info:
    #         total += entry[0]
    #     usage_count.append(total/len(usage_info))
    # usage_count.sort()
    # print(usage_count)
    # print(len(usage_count))
    # write_json("D:/data/data_copy/figure/datas/s_3_3_3.txt", usage_count)

    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_3.txt")
    # data_group(usage_count, 10, "The Average Usage Outdatedness of the Library Dependencies on a Library (#)","The Number of Libraries (#)", False)

    keys = [''] * 33
    values = [0] * 33
    keys[0] = '0'
    for i in range(0, 25):
        start = i * 2
        end = i * 2 + 2
        keys[i + 1] = str(start) + "-" + str(end)
    keys[26] = '50-60'
    keys[27] = '60-70'
    keys[28] = '70-80'
    keys[29] = '80-90'
    keys[30] = '90-100'
    keys[31] = '100-300'
    keys[32] = '300-2240'
    usage_count = read_json("D:/data/data_copy/figure/datas/s_3_3_3.txt")
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 300 and num <= 2240:
            values[32] += 1
        elif num > 100 and num <= 300:
            values[31] += 1
        elif num > 90 and num <= 100:
            values[30] += 1
        elif num > 80 and num <= 90:
            values[29] += 1
        elif num > 70 and num <= 80:
            values[28] += 1
        elif num > 60 and num <= 70:
            values[27] += 1
        elif num > 50 and num <= 60:
            values[26] += 1
        elif num == 0:
            values[0] += 1
        else:
            index = num // 2 + 1
            index = int(round(index, 0))
            if num % 2 == 0:
                index -= 1
            values[index] += 1
    # draw_bar(keys, values, "The Average Usage Outdatedness of the Library Dependencies on a Library (#)","The Number of Libraries (#)")


# project()
# s_3_1_1()
# s_3_1_2()
# s_3_1_3()
# s_3_1_4_1()
# s_3_1_4_2()
# s_3_1_5()
# s_3_1_6()
# s_3_1_7()
# lib_used_api()
# s_3_2_1()
# lib_percent()
# s_3_2_2()
# s_3_2_3()
s_3_3_1()
# s_3_3_2()
# s_3_3_3()
# outdateness()
# release()

