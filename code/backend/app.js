async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return res.json()
}

document.getElementById('create-form').addEventListener('submit', async (e) => {
  e.preventDefault()
  const title = document.getElementById('title').value
  const description = document.getElementById('description').value
  let attributes = {}
  try { attributes = JSON.parse(document.getElementById('attributes').value || '{}') } catch(e) { alert('Atributos JSON inválido'); return }
  const r = await postJSON('/listings', { title, description, attributes })
  document.getElementById('create-result').textContent = JSON.stringify(r, null, 2)
})

document.getElementById('predict-form').addEventListener('submit', async (e) => {
  e.preventDefault()
  const title = document.getElementById('ptitle').value
  const description = document.getElementById('pdescription').value
  let attributes = {}
  try { attributes = JSON.parse(document.getElementById('pattributes').value || '{}') } catch(e) { alert('Atributos JSON inválido'); return }
  const r = await postJSON('/predict', { title, description, attributes })
  document.getElementById('predict-result').textContent = JSON.stringify(r, null, 2)
})
