var cpcs = [' ', 'Abdominal distension', 'Abdominal pain', 'Abnormal behaviour', 'Abnormal vital sign(s)', 'Administration of medication', 'Aggressive behaviour', 'Alcohol/drug intoxication or withdrawal', 'Altered bowel habit', 'Altered mental state/confusion', 'Altered sensation', 'Anxiety', 'Ataxia', 'Back pain (no recent injury)', 'Bite', 'Blood in urine', 'Breast problem', 'Burn', 'Cardiac arrest', 'Cardiac arrest due to trauma', 'Certificate or paperwork requested', 'Change of dressing', 'Chemical exposure', 'Chest pain', 'Collapse/syncope', 'Complication of device (not catheter)', 'Complication of urinary catheter', 'Constipation', 'Cough', 'Coughing up blood', 'Crying baby', 'Cyanosis', 'Difficulty weight bearing', 'Discharge from ear', 'Discharge from eye', 'Dizziness/vertigo', 'Drowning', 'Earache', 'Electrical injury', 'Episodes of not breathing (apnoea)', 'Excessive urine output', 'Exposure to blood/body fluid', 'Exposure to communicable disease', 'Fall(s) - no significant injury', 'Feeding problem', 'Female genital problem', 'Fever symptoms', 'Follow-up visit', 'Foreign body in ear canal', 'Foreign body in eye', 'Foreign body in gastrointestinal tract (swallowed)', 'Foreign body in genitourinary tract', 'Foreign body in nose', 'Foreign body in rectum', 'Foreign body in respiratory tract (inhaled)', 'Foreign body in skin', 'Foreign body in throat', 'Frostbite', 'General weakness/fatigue/unwell', 'Headache', 'Hearing loss/tinnitus', 'Hiccoughs', 'Hyperglycaemia', 'Hypoglycaemia', 'Hypothermia', 'Increased muscle tone', 'Ingestion of potentially harmful substance', 'Injury of abdomen', 'Injury of back', 'Injury of buttock', 'Injury of chest', 'Injury of ear', 'Injury of eye', 'Injury of face', 'Injury of genitalia', 'Injury of head', 'Injury of hip', 'Injury of lower limb', 'Injury of neck', 'Injury of nose', 'Injury of perineum', 'Injury of upper limb', 'Insomnia', 'Itching', 'Jaundice', 'Labour', 'Localised lump/redness/swelling of skin', 'Loss of appetite', 'Male genital problem', 'Memory loss', 'Mental health problem', 'Mouth problem (not dental)', 'Multiple injuries - major', 'Multiple injuries - minor', 'Nasal congestion', 'Nausea/vomiting/diarrhoea', 'Neck pain (no recent injury)', 'Noisy breathing', 'Nose bleed', 'Noxious inhalation', 'Open wound (abrasion/laceration/puncture)', 'Overdose of drug', 'Pain in anus/rectum', 'Pain in breast', 'Pain in eye', 'Pain in face', 'Pain in hip', 'Pain in groin', 'Pain in lower limb (no recent injury)', 'Pain in upper limb (no recent injury)', 'Palpitations', 'Periods of not breathing', 'Photophobia', 'Plaster cast problem', 'Postoperative complication', 'Postpartum complication', 'Pregnancy problem', 'Rash', 'Rectal bleed', 'Red eye', 'Reduced urine output', 'Referral for investigation', 'Removal of skin sutures or staples', 'Respiratory arrest', 'Script request', 'Seizure', 'Self harm', 'Sexual assault', 'Shock from internal defibrillator', 'Shortness of breath', 'Situational crisis', 'Sore throat', 'Speech problem', 'Spontaneous bruising', 'Sting', 'Stoma problem', 'Suicidal thoughts', 'Swallowing problem', 'Swelling of face', 'Swelling of joint (no recent injury)', 'Swelling of tongue', 'Swollen leg (single)', 'Swollen legs (both)', 'Toothache/dental infection', 'Toxic inhalation injury', 'Tremor', 'UTI symptoms', 'Urethral discharge', 'Urinary retention', 'Vaginal bleeding - not pregnant', 'Vaginal discharge', 'Vascular disorder of limb', 'Visual disturbance', 'Vomiting blood', 'Weakness of face muscles', 'Weakness of limb', 'Wound complication']

d3.select("#cpc-button")
.selectAll('myOptions')
.data(cpcs)
.enter()
.append('option')
.text(function (d) { return d; }) 
.attr("value", function (d) { return d; })

d3.select("#cpc-button").on("change", function(d){
    window.PresentingComplaint = this.value
}
)
