(if (.input["Full name"] | split(" ") | length > 1) then (.input["Full name"] | split(" ") | .[0]) else (.input["Full name"]) end) as $given_name |
(if (.input["Full name"] | split(" ") | length > 1) then (.input["Full name"] | split(" ") | .[-1]) else ("") end) as $family_name |
(if (.input["Full name"] | split(" ") | length > 2) then (.input["Full name"] | split(" ") | .[1:-1] | join(" ")) else ("") end) as $addl_name |
.input as $input |
{
  "name": ($family_name | ascii_upcase),
  "is_group": true,
  "email": .input["Email id"],
  "address": .input["Address"],
  "program_memberships": [
    {
      "name": "Social Cash Transfer Programme [Digital payment]",
      "enrollment_date": "2024-02-15",
      "program_registrant_info": {
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
  "members": [
    {
      "name" : (((if $family_name!="" then $family_name + ", " else "" end) + (if $given_name!="" then $given_name + " " else "" end) + (if $addl_name!="" then $addl_name + " " else "" end)) | ascii_upcase),
      "given_name": $given_name,
      "family_name": $family_name, 
      "addl_name": $addl_name,
      "gender": .input["Gender"],
      "birthdate": (.input["Date of birth"] | strptime("%d-%m-%Y") | strftime("%Y-%m-%d") ),
      "ids": [
        {
          "id_type": "NATIONAL ID",
          "value": .input["Token ID"],
          "expiry_date": "2096-11-26"
        },
        {
          "id_type": "HOUSEHOLD ID",
          "value": (.input["Household Id"] | tostring),
          "expiry_date": "2090-02-26"
        }
      ],
      "kind": [
        {
          "name": "Head"
        }
      ],
      "is_group": false,
      "notification_preference": "none",
      "email": .input["Email id"],
      "address": .input["Address"]
    },
    {
      "name": (($family_name + ", " + "Alimayu" ) | ascii_upcase),
      "given_name": "Alimayu",
      "family_name": $family_name,
      "gender": "Male",
      "birthdate": "1999-05-24",
      "is_group": false,
      "notification_preference": "none",
      "address": .input["Address"]
    },
    {
      "name": (($family_name + ", " + "Liya" ) | ascii_upcase),
      "given_name": "Liya",
      "family_name": $family_name,
      "gender": "Female",
      "birthdate": "2022-04-18",
      "is_group": false,
      "notification_preference": "none",
      "address": .input["Address"]
    },
    {
      "name": (($family_name + ", " + "Negasi" ) | ascii_upcase),
      "given_name": "Negasi",
      "family_name": $family_name,
      "gender": "Male",
      "birthdate": "2021-09-10",
      "is_group": false,
      "notification_preference": "none",
      "address": .input["Address"]
    },
    {
      "name": (($family_name + ", " + "Zuri" ) | ascii_upcase),
      "given_name": "Zuri",
      "family_name": $family_name,
      "gender": "Female",
      "birthdate": "2023-01-12",
      "is_group": false,
      "notification_preference": "none",
      "address": .input["Address"]
    }
  ],
  "kind": "Household",
  "is_partial_group": false
}