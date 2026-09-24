# Revisión de avisos numéricos y HTML

Fuente: `2026-09-24T19-12-21-788Z`. Revisión: 24 de septiembre de 2026.
El auditor conserva las incidencias incluso cuando se justifican aquí.
Estas decisiones no certifican el resto de la prosa de cada página.

La normalización de separadores de miles reduce 114 avisos iniciales a 106.
No se normalizan automáticamente distancias o pesos: hacerlo podría ocultar
una conversión incorrecta. Cien páginas contienen unidades inglesas; necesitan
contraste contextual antes de cerrar su revisión numérica.

| Página / ID | Diferencia revisada | Decisión |
|---|---|---|
| What's Next, capítulo 3 / `kDodSyEJUYOo5Xmr` | `10 percent` → `diez por ciento` | Equivalente; conservar |
| Hobgoblin Quarters / `9I6vEKaSMk4uePzW` | `1 lb.` → `medio kilo` | Redondeo de peso; conservar por ahora y documentar criterio métrico del lote |
| Blighted Farmhouse / `YDPtsSj1aArP6AIQ` | `round 3` → `tercer asalto` | Equivalente; conservar |
| What's Next, capítulo 4 / `7g2ZWQD6JkswodUi` | `10 percent` → `diez por ciento` | Equivalente; conservar |
| Crypt Hauntings / `4WGf0GMNYJlIPjmd` | `d6` → `1d6` | Equivalente; conservar |
| Deepening Hall / `yxyyMpycWR6HIKnx` | Dos repeticiones de `T3` abreviadas en la prosa | El referente y el enlace T3 permanecen; conserva llegada tras 3 asaltos |

El único aviso de atributos HTML corresponde a `jGmKQG6znZFpZGhu`
(Cragmaw Hideout): cinco `data-tooltip` de monedas pasan de Platinum, Gold,
Electrum, Silver y Copper a Platino, Oro, Electro, Plata y Cobre. Son etiquetas
visibles traducibles; se mantienen los demás atributos y destinos.

No se han detectado diferencias en los destinos `@UUID`, instrucciones
`@Embed`, expresiones de tirada ni referencias reconocidas por el auditor.
Esto compara cadenas; no comprueba que todos los destinos se resuelvan en un
mundo importado ni demuestra equivalencia semántica de todo el HTML.
