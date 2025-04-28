$(document).ready(function () {
  $(".table").DataTable({
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
});


// Função para gerar o PDF
$("#download-pdf").on("click", function () {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Clona a tabela para manipulação sem afetar o frontend
  const tabelaOriginal = document.querySelector("#tabela-itens");
  const tabelaClone = tabelaOriginal.cloneNode(true);

  // Cria um contêiner temporário para renderizar a tabela clonada
  const tempDiv = document.createElement("div");
  tempDiv.style.position = "absolute";
  tempDiv.style.left = "-9999px";
  tempDiv.appendChild(tabelaClone);
  document.body.appendChild(tempDiv);


  // Adiciona o cabeçalho da nova coluna na penúltima posição
  const newColumnHeader = document.createElement("th");
  newColumnHeader.textContent = "Quantidade Comprada";
  // newColumnHeader.style.textAlign = "center";
  newColumnHeader.style.width = "50px";

  const headerRow = tabelaClone.querySelector("thead tr");
  const ths = headerRow.querySelectorAll("th");
  headerRow.insertBefore(newColumnHeader, ths[ths.length - 1]);

  // Adiciona a nova célula em cada linha do corpo na penúltima posição
  tabelaClone.querySelectorAll("tbody tr").forEach((row) => {
    const tds = row.querySelectorAll("td");
    const newCell = document.createElement("td");
    newCell.textContent = ""; // Célula vazia
    newCell.style.textAlign = "center";
    row.insertBefore(newCell, tds[tds.length - 1]);
  });

  // Remove o conteúdo da última coluna e adiciona um checkbox
  tabelaClone.querySelectorAll("tbody tr").forEach((row) => {
    const lastCell = row.lastElementChild;
    lastCell.innerHTML =
      '<input type="checkbox" style="transform: scale(1.5);">';
  });

  // Altera as cores da tabela clonada para preto
  tabelaClone.querySelectorAll("th, td").forEach((cell) => {
    cell.style.color = "black";
    cell.style.borderColor = "black";
  });

  // Captura a tabela clonada como imagem e gera o PDF
  html2canvas(tabelaClone)
    .then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const imgWidth = 190;
      const pageHeight = 295;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      const position = 10;

      doc.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
      const currentDate = new Date().toISOString().split("T")[0];
      doc.save(`itens_qtd_min_${currentDate}.pdf`);

      // Remove o contêiner temporário
      document.body.removeChild(tempDiv);
    })
    .catch((error) => {
      console.error("Erro ao gerar o PDF:", error);
    });
});
