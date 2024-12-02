document.getElementById('generatePDF').addEventListener('click', () => {
    const { jsPDF } = window.jspdf;

    // Captura o elemento HTML
    const content = document.getElementById('conteudo');
    
    // Captura o texto do protocolo (supondo que o id seja 'protocolo')
    let protocoloElement = document.getElementById('protocolo');
    let protocoloText = protocoloElement.textContent || protocoloElement.innerText;
    
    // Formata o protocolo removendo o texto antes do ':'
    let protocolo_formatado = protocoloText.split(":")[1].trim();

    // Converte o conteúdo HTML para imagem
    html2canvas(content).then((canvas) => {
        const imgData = canvas.toDataURL('image/png'); // Converte para imagem
        const pdf = new jsPDF(); // Cria o PDF

        // Calcula a largura e altura da imagem no PDF
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        // Adiciona a imagem ao PDF
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);

        // Salva o PDF com o nome do protocolo
        pdf.save(protocolo_formatado + ".pdf");
    });
});




setTimeout(() => {
    const messageBox = document.querySelector('.messages');
    if (messageBox) {
        messageBox.style.transition = 'opacity 1s ease-out';
        messageBox.style.opacity = '0';
        setTimeout(() => messageBox.remove(), 1000); // Remove do DOM após 1 segundo
    }
}, 5000); // 5000ms = 5 segundos