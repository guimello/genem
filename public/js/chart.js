google.load('visualization', '1', {packages: ['corechart']});

function drawVisualization(data) {
  var chart_data = [['Nota', 'Escola', 'Cidade']];
  var label, school_grade, city_grade;
  var chart_title = data.school.name.toLowerCase() +
    " vs " + data.city.name.toLowerCase() + " - SP";

  for (i = 0, length = data.school.relative_grades.length; i < length; i++) {
    label = i + "-" + (i + 1);
    school_grade = data.school.relative_grades[i] / 100;
    city_grade = data.city.relative_grades[i] / 100;

    chart_data[i + 1] = [label, school_grade, city_grade];
  }

  chart_data = google.visualization.arrayToDataTable(chart_data);

  // Formatting the tooltip
  var formatter = new google.visualization.NumberFormat({
    pattern: '#%',
    fractionDigits: 2
  });

  formatter.format(chart_data, 1);
  formatter.format(chart_data, 2);

  // Create and draw the visualization.
  new google.visualization.ColumnChart(document.getElementById('visualization')).
    draw(chart_data, {
          title: chart_title,
          width:800, height:400,
          hAxis: { title: "Nota" },
          vAxis: { title: "Frequência (%)", format:'#%' },
          bar: { groupWidth: "99%" }}
    );
}
