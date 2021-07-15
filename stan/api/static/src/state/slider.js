var painScale = ["Nil", "Mild", "Moderate", "Severe"];
var painScaleNumbers = [0, 1, 2, 3];
var painScaleSubmission = [0, 3, 6, 9];

var sliderPain = d3
  .sliderBottom()
  .min(d3.min(painScaleNumbers))
  .max(d3.max(painScaleNumbers))
  .width(300)
  .ticks(10)
  .step(1)
  .default(5)
  .on('onchange', val => {
    d3.select('p#value-pain').text((painScale[val]));
    observePainScale();
  });

var gPain = d3
  .select('div#slider-pain')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gPain.call(sliderPain);

d3.select('p#value-pain').text(painScale[sliderPain.value()]);


var disabilityScale = ["Alert", "Verbalises", "Responds to Pain", "Unconscious"];
var disabilityNumbers = [0, 1, 2, 3];
var disabilitySubmission = ["A", "V", "P", "U"]

var sliderDisability = d3
  .sliderBottom()
  .min(d3.min(disabilityNumbers))
  .max(d3.max(disabilityNumbers))
  .width(300)
  .ticks(4)
  .step(1)
  .on('onchange', val => {
    d3.select('p#value-disability').text(disabilityScale[val]);
    observeDisabilityValue();
  });

var gDisability = d3
  .select('div#slider-disability')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gDisability.call(sliderDisability);

d3.select('p#value-disability').text(disabilityScale[sliderDisability.value()]);


var vitalsignsScale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220];
  
var sliderVitalsigns = d3
  .sliderBottom()
  .min(d3.min(vitalsignsScale))
  .max(d3.max(vitalsignsScale))
  .width(300)
  .ticks(11)
  .step(1)
  .default(80)
  .on('onchange', val => {
    d3.select('p#value-vitalsigns').text((val));
    observeVitalSignsPulse();
  });

var gVitalsigns = d3
  .select('div#slider-vitalsigns')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gVitalsigns.call(sliderVitalsigns);

d3.select('p#value-vitalsigns').text((sliderVitalsigns.value()));



var respiratoryScale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60];
  
var sliderRespiratory = d3
  .sliderBottom()
  .min(d3.min(respiratoryScale))
  .max(d3.max(respiratoryScale))
  .width(300)
  .ticks(10)
  .step(1)
  .default(15)
  .on('onchange', val => {
    d3.select('p#value-respiratory').text((val));
    observeRespiratoryRate();
  });

var gRespiratory = d3
  .select('div#slider-respiratory')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gRespiratory.call(sliderRespiratory);

d3.select('p#value-respiratory').text((sliderRespiratory.value()));



var BloodPressureSystolicScale = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200];

var sliderBloodPressureSystolic = d3
  .sliderBottom()
  .min(d3.min(BloodPressureSystolicScale))
  .max(d3.max(BloodPressureSystolicScale))
  .width(300)
  .ticks(10)
  .step(1)
  .default(115)
  .on('onchange', val => {
    d3.select('p#value-BloodPressure-systolic').text((val));
    observeBloodPressure();
  });

var gBloodPressureSystolic = d3
  .select('div#slider-BloodPressure-systolic')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gBloodPressureSystolic.call(sliderBloodPressureSystolic);

d3.select('p#value-BloodPressure-systolic').text((sliderBloodPressureSystolic.value()));



var BloodPressureDiastolicScale = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140];

var sliderBloodPressureDiastolic = d3
  .sliderBottom()
  .min(d3.min(BloodPressureDiastolicScale))
  .max(d3.max(BloodPressureDiastolicScale))
  .width(300)
  .ticks(10)
  .step(1)
  .default(70)
  .on('onchange', val => {
    d3.select('p#value-BloodPressure-diastolic').text((val));
    observeBloodPressure();
  });

var gBloodPressureDiastolic = d3
  .select('div#slider-BloodPressure-diastolic')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

gBloodPressureDiastolic.call(sliderBloodPressureDiastolic);

d3.select('p#value-BloodPressure-diastolic').text((sliderBloodPressureDiastolic.value()));






const ageScale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100];
  
var sliderAge = d3
  .sliderBottom()
  .min(d3.min(ageScale))
  .max(d3.max(ageScale))
  .width(300)
  .ticks(14)
  .step(1)
  .default(40)
  .on('onchange', val => {
    d3.select('p#value-age').text((val));
    window.Age = sliderAge.value();
  });

var gAge = d3
  .select('div#slider-age')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

  gAge.call(sliderAge);

d3.select('p#value-age').text((sliderAge.value()));

var Age = sliderAge.value();


const temperatureScale = [28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0];
  
var sliderTemperature = d3
  .sliderBottom()
  .min(d3.min(temperatureScale))
  .max(d3.max(temperatureScale))
  .width(300)
  .ticks(14)
  .step(0.5)
  .default(37.0)
  .on('onchange', val => {
    d3.select('p#value-temperature').text((val));
    window.temperature = sliderTemperature.value();
    observeTemperature();
  });

var gTemperature = d3
  .select('div#slider-temperature')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

  gTemperature.call(sliderTemperature);

d3.select('p#value-temperature').text((sliderTemperature.value()));

var Temperature = sliderTemperature.value();


const satsScale = [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100];
  
var sliderSats = d3
  .sliderBottom()
  .min(d3.min(satsScale))
  .max(d3.max(satsScale))
  .width(300)
  .ticks(14)
  .step(1)
  .default(100)
  .on('onchange', val => {
    d3.select('p#value-sats').text((val));
    window.Sats = sliderSats.value();
    observeSats();
  });

var gSats = d3
  .select('div#slider-sats')
  .append('svg')
  .attr('width', 500)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)');

  gSats.call(sliderSats);

d3.select('p#value-sats').text((sliderSats.value()));

var Sats = sliderSats.value();