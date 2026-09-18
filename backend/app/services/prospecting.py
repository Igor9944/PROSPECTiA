DEMO_COMPANIES = [
    {
        "name": "NordLogistique SAS",
        "industry": "Transport",
        "city": "Lille",
        "country": "France",
        "employee_count": 180,
        "website": "https://nordlogistique.example",
        "description": "Opérateur logistique régional cherchant à digitaliser le suivi des tournées.",
        "company_type": "PME",
    },
    {
        "name": "Clinique des Quais",
        "industry": "Santé",
        "city": "Bordeaux",
        "country": "France",
        "employee_count": 95,
        "website": "https://clinique-quais.example",
        "description": "Établissement de santé privé, besoin de sécuriser le dossier patient.",
        "company_type": "PME",
    },
    {
        "name": "Atelier Lumina",
        "industry": "Industrie",
        "city": "Lyon",
        "country": "France",
        "employee_count": 42,
        "website": "https://lumina.example",
        "description": "Fabricant d'éclairage LED, ERP vieillissant et parc hétérogène.",
        "company_type": "PME",
    },
    {
        "name": "Banque Horizon",
        "industry": "Finance",
        "city": "Paris",
        "country": "France",
        "employee_count": 620,
        "website": "https://banque-horizon.example",
        "description": "Établissement financier régional, projet cybersécurité et SOC.",
        "company_type": "ETI",
    },
    {
        "name": "École Nova",
        "industry": "Éducation",
        "city": "Nantes",
        "country": "France",
        "employee_count": 70,
        "website": "https://ecole-nova.example",
        "description": "Groupe scolaire privé, migration Microsoft 365 et filtrage web.",
        "company_type": "PME",
    },
    {
        "name": "Retail Pulse",
        "industry": "Commerce",
        "city": "Marseille",
        "country": "France",
        "employee_count": 210,
        "website": "https://retailpulse.example",
        "description": "Enseigne retail, unification des caisses et du stock.",
        "company_type": "PME",
    },
    {
        "name": "GreenWatt",
        "industry": "Énergie",
        "city": "Toulouse",
        "country": "France",
        "employee_count": 310,
        "website": "https://greenwatt.example",
        "description": "Acteur énergie renouvelable, supervision industrielle et cloud.",
        "company_type": "ETI",
    },
    {
        "name": "Helvetic Data",
        "industry": "Technologie",
        "city": "Genève",
        "country": "Suisse",
        "employee_count": 55,
        "website": "https://helveticdata.example",
        "description": "Éditeur SaaS, recherche un infogéreur francophone.",
        "company_type": "PME",
    },
]


def search_demo_companies(filters) -> list[dict]:
    results = []
    keywords = (filters.keywords or "").lower()
    needs = (filters.needs or "").lower()
    for company in DEMO_COMPANIES:
        haystack = f"{company['name']} {company['industry']} {company['description']} {company['city']}".lower()
        if filters.industry and filters.industry.lower() not in company["industry"].lower():
            continue
        if filters.city and filters.city.lower() not in company["city"].lower():
            continue
        if filters.country and filters.country.lower() not in company["country"].lower():
            continue
        if filters.min_employees and company["employee_count"] < filters.min_employees:
            continue
        if filters.max_employees and company["employee_count"] > filters.max_employees:
            continue
        if filters.company_type and filters.company_type.lower() not in company["company_type"].lower():
            continue
        if keywords and keywords not in haystack:
            continue
        if needs and needs not in haystack:
            continue
        score = 50
        if company["industry"] in {"Technologie", "Informatique", "Finance", "Santé", "Énergie"}:
            score += 20
        if company["employee_count"] >= 50:
            score += 15
        if company["city"] in {"Paris", "Lyon", "Lille", "Nantes", "Toulouse"}:
            score += 10
        company_copy = {**company, "potential_score": min(100, score), "source": "demo"}
        results.append(company_copy)
    return results
