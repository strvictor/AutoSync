$(document).ready(function () {
  const tabela = $("#tabela-itens").DataTable({
    processing: true,
    pageLength: 10,
    paging: true,
    lengthChange: true,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
    responsive: true,
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    language: {
      lengthMenu: "Mostrar _MENU_ registros por página",
      zeroRecords: "Nada encontrado!",
      info: "Mostrando página _PAGE_ de _PAGES_",
      infoEmpty: "Nenhum registro disponível",
      infoFiltered: "(filtrado de _MAX_ registros no total)",
      search: "",
      paginate: {
        first: "Primeiro",
        last: "Último",
        next: "Próximo",
        previous: "Anterior",
      },
    },
    initComplete: function () {
      const searchBox = $("div.dataTables_filter input");
      searchBox.attr("placeholder", "O que deseja buscar?");
    },
  });

  // Filtragem por data
  $("#filtrar").on("click", function () {
    const dataInicial = $("#data-inicial").val();
    const dataFinal = $("#data-final").val();

    if (dataInicial && dataFinal) {
      tabela.draw(); // Atualiza a tabela
    }
  });

  // Customização do filtro de DataTables
  $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    const dataInicial = $("#data-inicial").val();
    const dataFinal = $("#data-final").val();
    const dataReabastecimento = data[3]; // Coluna de data (índice 3)

    if (dataInicial && dataFinal) {
      // Converte a data do HTML para um formato reconhecido pelo JavaScript
      const dataReabastecimentoDate = parseCustomDate(dataReabastecimento);
      const dataInicialDate = new Date(dataInicial + "T00:00:00"); // Adiciona hora inicial
      const dataFinalDate = new Date(dataFinal + "T23:59:59"); // Adiciona hora final

      if (!dataReabastecimentoDate) {
        console.error("Formato de data inválido:", dataReabastecimento);
        return false;
      }

      return (
        dataReabastecimentoDate >= dataInicialDate &&
        dataReabastecimentoDate <= dataFinalDate
      );
    }

    return true; // Mostra todas as linhas se não houver filtro
  });

  // Função para converter a data no formato "23 de Abril de 2025 às 18:54"
  function parseCustomDate(dateString) {
    const months = {
      Janeiro: 0,
      Fevereiro: 1,
      Março: 2,
      Abril: 3,
      Maio: 4,
      Junho: 5,
      Julho: 6,
      Agosto: 7,
      Setembro: 8,
      Outubro: 9,
      Novembro: 10,
      Dezembro: 11,
    };

    const regex = /(\d{1,2}) de (\w+) de (\d{4}) às (\d{2}):(\d{2})/;
    const match = dateString.match(regex);

    if (match) {
      const day = parseInt(match[1], 10);
      const month = months[match[2]];
      const year = parseInt(match[3], 10);
      const hours = parseInt(match[4], 10);
      const minutes = parseInt(match[5], 10);

      return new Date(year, month, day, hours, minutes);
    }

    return null; // Retorna null se o formato não for válido
  }
});

$("#exportar-excel").on("click", function () {
  const tabela = document.getElementById("tabela-itens");
  const wb = XLSX.utils.table_to_book(tabela, { sheet: "Reabastecimentos" });
  XLSX.writeFile(wb, "ultimos_reabastecimentos.xlsx");
});
