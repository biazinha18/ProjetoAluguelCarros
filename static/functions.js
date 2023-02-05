function toggleMenu(event) {
  if (event.type === 'touchstart') event.preventDefault();
  const nav = document.getElementById('nav');
  nav.classList.toggle('active');
  const active = nav.classList.contains('active');
  event.currentTarget.setAttribute('aria-expanded', active);
  if (active) {
    event.currentTarget.setAttribute('aria-label', 'Fechar Menu');
  } else {
    event.currentTarget.setAttribute('aria-label', 'Abrir Menu');
  }
}

function add_update_car(method, formid, variable){
  var base_request_url = '/carros'
  const form = document.querySelector('#'+formid);
  const data = Object.fromEntries(new FormData(form).entries());
  console.log(data)
  if(method == 'PUT')
    base_request_url = base_request_url + "/" + data[variable]
  
  var list = JSON.stringify(data);

  $.ajax({
      type: method,
      url: base_request_url,
      data: list,
      dataType: "json",
      contentType: "application/json"
  });
}

function delete_car(id){
  $.ajax({
    type: 'DELETE',
    url: '/carros/'+id
  });
  window.location.reload();
}

function find_car(){
  const modelo = document.getElementById('modelo').value;
  const ano = document.getElementById('ano').value;
  window.location.href = 'carros/'+modelo+'/'+ano;
}

$.get("/carros", function(data, status){
  let placeholder = document.querySelector('#grid');
  let out = "";
  for (let carro of data['carros']){
    out += `
      <div class="carro">
        <div class="left-carro">
            <img src="${carro.image}">
        </div>
        <div class="right-carro">
            <ul>
                <li>Modelo: ${carro.modelo}</li>
                <li>Marca: ${carro.marca}</li>
                <li>Ano: ${carro.ano}</li>
                <li>Valor Diária: R$ ${carro.valor}</li>
                <li>Status: ${carro.status}</li>
            </ul>
            <button onclick="location.href='update/${carro.modelo}/${carro.ano}'">Atualizar</button> 
            <button onclick="delete_car(${carro.id})">Deletar</button>
        </div>
      </div>
    `;
  }
  placeholder.innerHTML = out;
});
