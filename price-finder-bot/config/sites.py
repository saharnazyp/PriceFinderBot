"""Registry of target sites with scraping priority.

Priority rationale:
  1. torob (aggregator covering hundreds of stores -> highest efficiency)
  2. digikala, basalam
  3. wholesale / omde sites
  4. app-heavy / JS-heavy sites (okala, snappshop) LAST -> geolocation pricing
"""

SITES = [
    # (key, domain, priority, notes)
    ("torob",        "torob.com",         1, "aggregator"),
    ("digikala",     "digikala.com",      2, "marketplace"),
    ("emalls",       "emalls.ir",         2, "price aggregator"),
    ("omde_bazar",   "omde-bazar.ir",     3, "wholesale"),
    ("omdehbazar",   "omdehbazar.com",    3, "wholesale"),
    ("bazarmolavi",  "bazarmolavi.com",   3, "wholesale"),
    ("sarayekharid", "sarayekharid.com",  3, "wholesale"),
    ("hyper_bazar",  "hyper-bazar.com",   3, "wholesale"),
    ("aghsami",      "aghsami.ir",        3, "wholesale"),
    ("kitline",      "kitline.com",       3, "supplier"),
    ("shirreza",     "shirreza.com",      3, "supplier"),
    ("kassitsyrup",  "kassitsyrup.ir",    3, "supplier"),
    ("baradland",    "baradland.com",     3, "supplier"),
    ("digimeidoun",  "digimeidoun.ir",    3, "supplier"),
    ("sarvban",      "sarvban.com",       3, "supplier"),
    ("mazid",        "mazid.ir",          3, "supplier"),
    ("modiseh",      "modiseh.com",       3, "marketplace"),
    ("choconik",     "choconik.com",      3, "supplier"),
    ("okala",        "okala.com",         4, "app-heavy, geo pricing"),
    ("snappshop",    "snappshop.ir",      4, "app-heavy, geo pricing"),
]

SITES_BY_PRIORITY = sorted(SITES, key=lambda s: s[2])
