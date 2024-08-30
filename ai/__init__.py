DB_DESCRIPTION = """
Table name: customers - This table contains comprehensive customer data including demographics, service subscriptions, billing information, and churn-related metrics for a telecommunications company.

customer_id: A unique ID that identifies each customer.

gender: The customer's gender: Male, Female

age: The customer's current age, in years, at the time the fiscal quarter ended.

under_30: Indicates if the customer is under 30 years old: Yes, No

senior_citizen: Indicates if the customer is 65 or older: Yes, No

married: Indicates if the customer is married: Yes, No

dependents: Indicates if the customer lives with any dependents: Yes, No. Dependents could be children, parents, grandparents, etc.

number_of_dependents: Indicates the number of dependents that live with the customer.

customer_id: A unique ID that identifies each customer.

count: A value used in reporting/dashboarding to sum up the number of customers in a filtered set.

country: The country of the customer's primary residence.

state: The state of the customer's primary residence.

city: The city of the customer's primary residence.

zip_code: The zip code of the customer's primary residence.

latitude: The latitude of the customer's primary residence.

longitude: The longitude of the customer's primary residence.

zip_code: The zip code of the customer's primary residence.

population: A current population estimate for the entire Zip Code area.

customer_id: A unique ID that identifies each customer.

count: A value used in reporting/dashboarding to sum up the number of customers in a filtered set.

quarter: The fiscal quarter that the data has been derived from (e.g. Q3).

referred_a_friend: Indicates if the customer has ever referred a friend or family member to this company: Yes, No

number_of_referrals: Indicates the number of referrals to date that the customer has made.

tenure_in_months: Indicates the total amount of months that the customer has been with the company by the end of the quarter specified above.

offer: Identifies the last marketing offer that the customer accepted, if applicable. Values include None, Offer A, Offer B, Offer C, Offer D, and Offer E.

phone_service: Indicates if the customer subscribes to home phone service with the company: Yes, No

avg_monthly_long_distance_charges: Indicates the customer's average long distance charges, calculated to the end of the quarter specified above.

multiple_lines: Indicates if the customer subscribes to multiple telephone lines with the company: Yes, No

internet_service: Indicates if the customer subscribes to Internet service with the company: No, DSL, Fiber Optic, Cable.

avg_monthly_gb_download: Indicates the customer's average download volume in gigabytes, calculated to the end of the quarter specified above.

online_security: Indicates if the customer subscribes to an additional online security service provided by the company: Yes, No

online_backup: Indicates if the customer subscribes to an additional online backup service provided by the company: Yes, No

device_protection_plan: Indicates if the customer subscribes to an additional device protection plan for their Internet equipment provided by the company: Yes, No

premium_tech_support: Indicates if the customer subscribes to an additional technical support plan from the company with reduced wait times: Yes, No

streaming_tv: Indicates if the customer uses their Internet service to stream television programing from a third party provider: Yes, No. The company does not charge an additional fee for this service.

streaming_movies: Indicates if the customer uses their Internet service to stream movies from a third party provider: Yes, No. The company does not charge an additional fee for this service.

streaming_music: Indicates if the customer uses their Internet service to stream music from a third party provider: Yes, No. The company does not charge an additional fee for this service.

unlimited_data: Indicates if the customer has paid an additional monthly fee to have unlimited data downloads/uploads: Yes, No

contract: Indicates the customer's current contract type: Month-to-Month, One Year, Two Year.

paperless_billing: Indicates if the customer has chosen paperless billing: Yes, No

payment_method: Indicates how the customer pays their bill: Bank Withdrawal, Credit Card, Mailed Check

monthly_charge: Indicates the customer's current total monthly charge for all their services from the company.

total_charges: Indicates the customer's total charges, calculated to the end of the quarter specified above.

total_refunds: Indicates the customer's total refunds, calculated to the end of the quarter specified above.

total_extra_data_charges: Indicates the customer's total charges for extra data downloads above those specified in their plan, by the end of the quarter specified above.

total_long_distance_charges: Indicates the customer's total charges for long distance above those specified in their plan, by the end of the quarter specified above.

customer_id: A unique ID that identifies each customer.

count: A value used in reporting/dashboarding to sum up the number of customers in a filtered set.

quarter: The fiscal quarter that the data has been derived from (e.g. Q3).

satisfaction_score: A customer's overall satisfaction rating of the company from 1 (Very Unsatisfied) to 5 (Very Satisfied).

satisfaction_score_label: Indicates the text version of the score (1-5) as a text string.

customer_status: Indicates the status of the customer at the end of the quarter: Churned, Stayed, or Joined

churn_label: Yes = the customer left the company this quarter. No = the customer remained with the company. Directly related to Churn Value.

churn_value: 1 = the customer left the company this quarter. 0 = the customer remained with the company. Directly related to Churn Label.

churn_score: A value from 0-100 that is calculated using the predictive tool IBM SPSS Modeler. The model incorporates multiple factors known to cause churn. The higher the score, the more likely the customer will churn.

churn_score_category: A calculation that assigns a Churn Score to one of the following categories: 0-10, 11-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-80, 81-90, and 91-100

cltv: Customer Lifetime Value. A predicted CLTV is calculated using corporate formulas and existing data. The higher the value, the more valuable the customer. High value customers should be monitored for churn.

cltv_category: A calculation that assigns a CLTV value to one of the following categories: 2000-2500, 2501-3000, 3001-3500, 3501-4000, 4001-4500, 4501-5000, 5001-5500, 5501-6000, 6001-6500, and 6501-7000.

churn_category: A high-level category for the customer's reason for churning: Attitude, Competitor, Dissatisfaction, Other, Price. When they leave the company, all customers are asked about their reasons for leaving. Directly related to Churn Reason.

churn_reason: A customer's specific reason for leaving the company. Directly related to Churn Category.
"""

COLUMN_NAME_MAPPING = {
    "Customer ID": "customer_id",
    "Gender": "gender",
    "Age": "age",
    "Under 30": "under_30",
    "Senior Citizen": "senior_citizen",
    "Married": "married",
    "Dependents": "dependents",
    "Number of Dependents": "number_of_dependents",
    "Country": "country",
    "State": "state",
    "City": "city",
    "Zip Code": "zip_code",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Population": "population",
    "Quarter": "quarter",
    "Referred a Friend": "referred_a_friend",
    "Number of Referrals": "number_of_referrals",
    "Tenure in Months": "tenure_in_months",
    "Offer": "offer",
    "Phone Service": "phone_service",
    "Avg Monthly Long Distance Charges": "avg_monthly_long_distance_charges",
    "Multiple Lines": "multiple_lines",
    "Internet Service": "internet_service",
    "Internet Type": "internet_type",
    "Avg Monthly GB Download": "avg_monthly_gb_download",
    "Online Security": "online_security",
    "Online Backup": "online_backup",
    "Device Protection Plan": "device_protection_plan",
    "Premium Tech Support": "premium_tech_support",
    "Streaming TV": "streaming_tv",
    "Streaming Movies": "streaming_movies",
    "Streaming Music": "streaming_music",
    "Unlimited Data": "unlimited_data",
    "Contract": "contract",
    "Paperless Billing": "paperless_billing",
    "Payment Method": "payment_method",
    "Monthly Charge": "monthly_charge",
    "Total Charges": "total_charges",
    "Total Refunds": "total_refunds",
    "Total Extra Data Charges": "total_extra_data_charges",
    "Total Long Distance Charges": "total_long_distance_charges",
    "Total Revenue": "total_revenue",
    "Satisfaction Score": "satisfaction_score",
    "Customer Status": "customer_status",
    "Churn Label": "churn_label",
    "Churn Score": "churn_score",
    "CLTV": "cltv",
    "Churn Category": "churn_category",
    "Churn Reason": "churn_reason"
}