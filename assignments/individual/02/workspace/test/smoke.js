// End-to-end smoke test against a running server (npm start or npm run start:memory).
//   node test/smoke.js            -> uses http://localhost:5000
//   API_URL=http://... node test/smoke.js
const API = process.env.API_URL || 'http://localhost:5000'
let failures = 0

async function call(method, path, body) {
  const res = await fetch(API + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined
  })
  let json = null
  try { json = await res.json() } catch {}
  return { status: res.status, body: json }
}

function check(label, cond, extra = '') {
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${label}${extra ? '  -> ' + extra : ''}`)
  if (!cond) failures++
}

async function main() {
  const plan = {
    name: 'Smoke Test Layout',
    venue: 'Test venue',
    extraPersonFee: 600,
    landmarks: [{ name: 'STAGE', position: { x: 1, y: 1 } }],
    zones: [
      {
        name: 'Zone A',
        pricing: [{ type: 'circle', packagePrice: 2400, package: '1 TOWER + 1 ICE' }, { type: 'sofa', packagePrice: 7200 }],
        tables: [{ number: 'A1', type: 'circle' }, { number: 'A2', type: 'sofa' }]
      },
      {
        name: 'Zone B',
        pricing: [{ type: 'triangle', packagePrice: 700 }],
        tables: [{ number: 'T1', type: 'triangle' }]
      }
    ]
  }

  const before = await call('GET', '/floorplans')
  check('GET all returns 200 + array', before.status === 200 && Array.isArray(before.body), `${before.body?.length} plans`)

  const created = await call('POST', '/floorplans', plan)
  check('POST returns 201', created.status === 201, created.body?.message)
  const id = created.body?._id
  check('POST fills capacity from type', created.body?.zones?.[0]?.tables?.[1]?.capacity === 6 && created.body?.zones?.[1]?.tables?.[0]?.capacity === 1)
  check('POST computes tableCount / totalCapacity', created.body?.tableCount === 3 && created.body?.totalCapacity === 9)
  check('zones / tables / pricing are value objects (no _id)',
    created.body?.zones?.[0]?._id === undefined && created.body?.zones?.[0]?.tables?.[0]?._id === undefined && created.body?.zones?.[0]?.pricing?.[0]?._id === undefined)
  check('POST stores pricing and extraPersonFee', created.body?.zones?.[0]?.pricing?.[0]?.packagePrice === 2400 && created.body?.extraPersonFee === 600)

  const one = await call('GET', `/floorplans/${id}`)
  check('GET one returns 200 + same id', one.status === 200 && one.body?._id === id)

  const after = await call('GET', '/floorplans')
  check('GET all count grew by 1', after.body?.length === before.body.length + 1)

  const put = await call('PUT', `/floorplans/${id}`, {
    name: 'Smoke Test Layout v2',
    status: 'active',
    zones: [{ name: 'Zone A', pricing: [{ type: 'square', packagePrice: 4800 }], tables: [{ number: 'A1', type: 'square' }] }]
  })
  check('PUT returns 200 + replaced fields', put.status === 200 && put.body?.name === 'Smoke Test Layout v2' && put.body?.status === 'active', put.body?.message)
  check('PUT drops omitted fields (landmarks, venue, extraPersonFee)', put.body?.landmarks?.length === 0 && put.body?.venue === '' && put.body?.extraPersonFee === 0 && put.body?.zones?.length === 1)

  const patch = await call('PATCH', `/floorplans/${id}`, { status: 'draft' })
  check('PATCH changes only status', patch.status === 200 && patch.body?.status === 'draft' && patch.body?.name === 'Smoke Test Layout v2')

  const del = await call('DELETE', `/floorplans/${id}`)
  check('DELETE returns 200', del.status === 200)
  const gone = await call('GET', `/floorplans/${id}`)
  check('GET after DELETE returns 404', gone.status === 404)

  // error cases
  check('GET bad id -> 400', (await call('GET', '/floorplans/nope')).status === 400)
  check('GET unknown id -> 404', (await call('GET', '/floorplans/66f00000000000000000ffff')).status === 404)
  check('POST missing fields -> 400', (await call('POST', '/floorplans', { zones: [] })).status === 400)
  const dup = await call('POST', '/floorplans', {
    name: 'dup', zones: [
      { name: 'Z1', pricing: [{ type: 'square', packagePrice: 1 }], tables: [{ number: 'X1', type: 'square' }] },
      { name: 'Z2', pricing: [{ type: 'circle', packagePrice: 1 }], tables: [{ number: 'X1', type: 'circle' }] }
    ]
  })
  check('POST duplicate table number -> 400', dup.status === 400 && /Duplicate table/.test(dup.body?.message || ''), dup.body?.message)
  const dupZone = await call('POST', '/floorplans', {
    name: 'dupzone', zones: [
      { name: 'Z1', pricing: [{ type: 'square', packagePrice: 1 }], tables: [{ number: 'X1', type: 'square' }] },
      { name: 'Z1', pricing: [{ type: 'circle', packagePrice: 1 }], tables: [{ number: 'X2', type: 'circle' }] }
    ]
  })
  check('POST duplicate zone name -> 400', dupZone.status === 400 && /Duplicate zone/.test(dupZone.body?.message || ''), dupZone.body?.message)
  check('POST invalid type -> 400', (await call('POST', '/floorplans', { name: 'x', zones: [{ name: 'Z', pricing: [{ type: 'circle', packagePrice: 1 }], tables: [{ number: 'Y1', type: 'booth' }] }] })).status === 400)
  const unpriced = await call('POST', '/floorplans', {
    name: 'unpriced', zones: [{ name: 'Z', pricing: [{ type: 'circle', packagePrice: 2400 }], tables: [{ number: 'A1', type: 'circle' }, { number: 'A2', type: 'sofa' }] }]
  })
  check('POST table type without zone pricing -> 400', unpriced.status === 400 && /no pricing/.test(unpriced.body?.message || ''), unpriced.body?.message)

  const final = await call('GET', '/floorplans')
  check('collection back to original count', final.body?.length === before.body.length)

  console.log(failures ? `\n${failures} check(s) FAILED` : '\nAll checks passed')
  process.exit(failures ? 1 : 0)
}

main().catch((err) => { console.error('Cannot reach API:', err.message); process.exit(1) })
