function drawVisualization(data) {
  var chart_data = [[], []];
  var chart_title = data.school.name.toLowerCase() +
    " vs " + data.city.name.toLowerCase() + " - SP";

  for (i = 0, length = data.school.relative_grades.length; i < length; i++) {
    chart_data[0][i] = { y: data.school.relative_grades[i], grade: data.school.grades[i] };
    chart_data[1][i] = { y: data.city.relative_grades[i], grade: data.city.grades[i] };
  }

  $('#visualization').highcharts({
    chart: {
      type: 'column'
    },
    title: {
      text: chart_title,
      margin: 30
    },
    subtitle: {
      text: 'Competência Ciências da Natureza'
    },
    xAxis: {
      title: {
        text: 'Nota'
      },
      categories: [
          '0-1',
          '1-2',
          '2-3',
          '3-4',
          '4-5',
          '5-6',
          '6-7',
          '7-8',
          '8-9',
          '9-10'
      ]
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Frequência de alunos (%)'
      },
      labels: {
        formatter: function() {
          return this.value + " %";
        }
      }
    },
    tooltip: {
      formatter: function() {
        return "Relativo: <b>" +
          Highcharts.numberFormat(this.y, 2, ",") +
          " %</b><br/>Absoluto: <b>" +
          Highcharts.numberFormat(this.point.grade, 0, ",", ".") +
          " alunos</b>";
      }
    },
    plotOptions: {
      column: {
        pointPadding: 0,
        groupPadding: 0,
        borderWidth: 0
      }
    },
    series: [{
      name: 'Escola',
      data: chart_data[0]
    }, {
      name: 'São Paulo - SP',
      data: chart_data[1]
    }]
  });
}
