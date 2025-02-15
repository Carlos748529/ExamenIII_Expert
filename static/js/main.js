document.getElementById('diagnosticoForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const datos = {};
    
    for (let [key, value] of formData.entries()) {
        datos[key] = true;
    }

    // Agregar los síntomas no marcados como false
    ['fiebre', 'tos', 'dolor_garganta', 'dolor_abdominal', 'nauseas', 'vomito', 'erupcion'].forEach(sintoma => {
        if (!datos[sintoma]) {
            datos[sintoma] = false;
        }
    });

    try {
        const response = await fetch('/diagnosticar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        const result = await response.json();
        
        const resultadoContainer = document.getElementById('resultadoContainer');
        const diagnosticoResultado = document.getElementById('diagnosticoResultado');
        const infoAdicional = document.getElementById('infoAdicional');

        diagnosticoResultado.innerHTML = `<h5>Diagnóstico:</h5><p>${result.diagnostico}</p>`;
        
        if (result.info_adicional) {
            infoAdicional.innerHTML = `
                <h5>Información Adicional:</h5>
                <div class="alert alert-info">
                    ${result.info_adicional.summary || 'No hay información adicional disponible.'}
                </div>
            `;
        } else {
            infoAdicional.innerHTML = '';
        }

        resultadoContainer.classList.remove('d-none');
        resultadoContainer.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un error al procesar su solicitud.');
    }
}); 