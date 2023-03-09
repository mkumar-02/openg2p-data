(if (.input["Full name"] | split(" ") | length > 1) then (.input["Full name"] | split(" ") | .[0]) else (.input["Full name"]) end) as $given_name |
(if (.input["Full name"] | split(" ") | length > 1) then (.input["Full name"] | split(" ") | .[-1]) else ("") end) as $family_name |
(if (.input["Full name"] | split(" ") | length > 2) then (.input["Full name"] | split(" ") | .[1:-1] | join(" ")) else ("") end) as $addl_name |
{
  "given_name": $given_name,
  "family_name": $family_name, 
  "addl_name": $addl_name,
  "name" :  (((if $family_name!="" then $family_name + ", " else "" end) + (if $given_name!="" then $given_name + " " else "" end) + (if $addl_name!="" then $addl_name + " " else "" end)) | ascii_upcase),
  "ids": [
    {
      "id_type": "HOUSEHOLD ID",
      "value": (.input["Household Id"] | tostring),
      "expiry_date": "2090-02-26"
    },
    {
      "id_type": "MOSIP UIN TOKEN",
      "value": (.input["Token ID"] | tostring),
      "expiry_date": "2090-02-26"
    },
    {
      "id_type": "ACCOUNT_ID",
      "value": (.input["Account number"] | tostring),
      "expiry_date": "2090-02-26"
    }
  ],
  "phone_numbers": [
    {
      "phone_no": .input["Phone number"]
    }
  ],
  "email": .input["Email id"],
  "address": .input["Address"],
  "additional_g2p_info": [
    {
      "id": 2,
      "name": "Safety Net Program",
      "data": {
         "Is Consent Available?": true,
         "Household Id": (.input["Household Id"] | tostring),
         "Household size": .input["Household size"],
         "No of children": .input["No. of children"],
         "Own home?": (.input["Own home?"]=="yes"),
         "Size of home": .input["Size of home (sq. ft)"],
         "Employment status": .input["Employement status"],
         "Annual household income": .input["Annual household income (USD)"],
         "Vehicles owned": .input["Vehicles owned"],
         "Disablity status": .input["Disability status"],
         "Immigration status": .input["Immigration status"]
      }
    }
  ],
  "gender": .input["Gender"],
  "birthdate": (.input["Date of birth"] | strptime("%d-%m-%Y") | strftime("%Y-%m-%d") )
}
