def calculate_deduction(country,gross_salary):
    if country=="India":
        return gross_salary*0.10
    if country=="United States":
        return gross_salary*0.12
    return 0

def calculate_salary_details(country,gross_salary):
    deduction=calculate_deduction(country,gross_salary)
    net_salary=gross_salary-deduction
    return {"gross_salary":gross_salary,
            "deduction":deduction,
            "net_salary":net_salary}
