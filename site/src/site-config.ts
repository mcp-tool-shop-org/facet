import type { SiteConfig } from '@mcptoolshop/site-theme';

const REPO = 'https://github.com/mcp-tool-shop-org/facet';
// (the record lives on GitHub; handbook pages link to it directly)

export const config: SiteConfig = {
  title: 'facet — styled 2D concept to textured 3D asset',
  description:
    'A local, licence-clean route from a form-exaggerated clay concept to a textured 3D asset, with the style applied on the asset in texture space rather than painted per view. Four accepted assets across four subject classes, at zero credits.',
  logoBadge: 'FA',
  brandName: 'facet',
  repoUrl: REPO,
  footerText:
    'MIT Licensed — built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>. Every number on this page is measured and links to the ruling that established it.',

  hero: {
    badge: 'Four accepted assets · four subject classes · zero credits',
    headline: 'A styled 2D concept becomes a',
    headlineAccent: 'textured 3D asset.',
    description:
      'The style is applied <strong>on the asset</strong>, in texture space — not painted per view and stitched. Runs entirely on local hardware, with no non-commercial dependency anywhere in the chain.<br><br>Named for both halves of the problem: the polygons, and the face they have to hold.',
    primaryCta: { href: `${REPO}/tree/main/docs/experiments`, label: 'Read the record' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      {
        label: 'Weld, then allocate density',
        code: 'python tools/smart_decimate.py --target 150000',
      },
      {
        label: 'Twin this mesh, then project',
        code: 'python tools/project_twins.py --prep prep/ --out state/',
      },
      {
        label: 'Ask the record',
        code: 'python tools/facet_index.py q "blade band"',
      },
    ],
  },

  sections: [
    {
      kind: 'data-table',
      id: 'assets',
      title: 'Four accepted assets, four subject classes',
      subtitle:
        'Every one ruled by the Director at his own zoom — on the GLB, or on full-size sheets. Not a metric clearing a threshold. The mix is reference / brush / dilation as a share of valid texels, and those shares are NOT comparable across subjects: a ship hides most of itself from eye level and an animal hides half. Read each against its own pre-registered reach ceiling, against which they land 86–93% — the difference between the rows is geometry, not regression.',
      columns: ['Subject', 'Class', 'Accepted', 'Reference / brush / dilation, of valid', 'Ruling'],
      rows: [
        ['Character (W3)', 'humanoid', '2026-08-04', '68.8 / 4.2 / 27.0', 'E08 Amendment 35'],
        ['Galleon', 'vehicle · thin rigging', '2026-08-05', '36.89 / 6.87 / 56.24', 'E04 Ruling 29'],
        ['Dragon', 'beast · wing membranes', '2026-08-07', '44.15 / 3.07 / 52.78', 'E12 Ruling 28'],
        ['Longsword', 'prop · near-2D, grey-on-grey', '2026-08-08', '45.25 / 2.07 / 52.68', 'E14 Ruling 32'],
      ],
    },
    {
      kind: 'features',
      id: 'why',
      title: 'What makes it work',
      subtitle: 'Six findings that each cost an experiment, and each generalise.',
      features: [
        {
          title: 'Form first, style second',
          desc: 'Image-to-3D reconstructors read surface noise as geometry. A heavily stylized sprite fights the reconstructor; a clean sculpt-like clay with exaggerated planes comes back with better topology. The styled twin is generated alongside, and stays as the colour reference.',
        },
        {
          title: 'Twins belong to a mesh',
          desc: 'A styled twin carries the silhouette of the mesh it was rendered from. Reuse one across meshes and coverage collapses 62% → 22.7%, because the arms and sword project into empty space. Generate twins from the mesh you are about to texture — every time.',
        },
        {
          title: 'Identity belongs to the prompt',
          desc: 'Contradict the specification on eight named elements and the prompt wins 8 of 8 — median ΔE 46.3 against 6.2 on held controls. The mesh and control hold structure; named attributes ride the prompt. A canon element not named in the prompt arrived by accident and will leave the same way.',
        },
        {
          title: 'Ask geometry, not a threshold',
          desc: 'Corner-median keying failed three times here — painted art has a gradient, clay is grey on grey, diffusion paints a lit backdrop. Replacing the key with the exact raycast silhouette moved reference coverage 28.4% → 39.1% of valid texels, strictly additive, with no diffusion and no GPU.',
        },
        {
          title: 'Cull from the atlas, never the mesh',
          desc: '49% of atlas texels are never visible from outside. Excluding those faces from the UV layout cut interpolation 68%. Excluding rather than deleting makes the failure impossible instead of detectable — deletion needs a perfect gate forever, and the obvious gate scored 1.00000 on a mesh with a hole through the torso.',
        },
        {
          title: 'Gate the failure mode, not the success mode',
          desc: 'The recurring lesson. A gate written against what the operation looks like when it works will pass a broken artifact confidently. Ask what it looks like when it goes wrong, then check for that — and if the quantity you care about is measurable, gate on it rather than on a proxy for it.',
        },
      ],
    },
    {
      kind: 'features',
      id: 'method',
      title: 'How the repo is run',
      subtitle:
        'The discipline is the product as much as the pipeline is. It exists because an earlier arc ran ten sessions that each judged their own output and wrote conclusions the next session read as fact.',
      features: [
        {
          title: 'Spec before, report after, ruling last',
          desc: 'Every non-trivial change runs as a numbered experiment. The session that designs an experiment does not grade its results, and the session that runs it does not decide what they mean. Forty-four experiments are in the record, each with its predictions stated before the measurement.',
        },
        {
          title: 'Corrections in place, never deletions',
          desc: 'A claim that turns out wrong stays, annotated with the measurement that overturned it — because the correction is more useful than a tidy page. Six inherited claims were falsified in the founding session alone, and each one is still readable beside what replaced it.',
        },
        {
          title: 'Failures stay next to the code',
          desc: 'tools/superseded/ is not an archive. It is the mechanism that stops a falsified approach quietly becoming doctrine again — anyone can run those tools and watch them fail the same way, with the reason written down.',
        },
        {
          title: 'A negative result is a full success',
          desc: 'Arms that halt at their own pre-registered gates are reported and closed rather than tuned toward a number. One arm cut dilation source distance 70× and changed nothing to the eye — that measurement redirected four experiments’ worth of work.',
        },
        {
          title: 'The record is queryable',
          desc: 'A SQLite + FTS5 index over the whole trail, verified on four legs: byte-identical determinism across interpreters, counts against independent greps, zero dangling pointers, and a seeded question gate that grows with the record. It found a ruling count the prose had wrong at three sites, by counting the record itself.',
        },
        {
          title: 'Tests ride the commit',
          desc: '1098 tests passing at two seats’ hands, with paths-gated CI on the 1053 hermetic ones. A commit that changes tool code carries tests for that code in the same commit; recorded anchors are ported into the harness rather than left in reports.',
        },
      ],
    },
    {
      kind: 'data-table',
      id: 'honest',
      title: 'What is not solved',
      subtitle:
        'Named, measured, located in code, and left on the front page. A page that only lists wins is not a status report.',
      columns: ['Defect', 'Measured', 'Where'],
      rows: [
        [
          'The blade band carries no stage-1 reference',
          '0.00% per view on all eight cameras; the union rescues 55.72%. Steel on a grey backdrop sits on the key’s own threshold.',
          'A global 0.06 cut governing a local low-contrast feature',
        ],
        [
          'Stroke seams are not levelled',
          'A provenance boundary steps 5.5× ordinary texture variation; the region the Director named steps 9.5×.',
          'texpass_iter.py — commit writes colour with no levelling term',
        ],
        [
          'Dilation bleeds between unrelated islands',
          '74.9% of 813,773 dilated texels take colour from another island, from a median 0.177 away on a figure 1.0 tall.',
          'texpass_finalize.py — the flood predicate has no & valid',
        ],
        [
          'Reconstructions are hollow double-walled shells',
          'Walls ~two voxels around an empty cavity, measured three independent ways with two accepted assets as controls.',
          'A route-wide property — no volumetric predicate is valid on them',
        ],
      ],
    },
    {
      kind: 'code-cards',
      id: 'licence',
      title: 'Licence position',
      subtitle:
        'Every stage runs local and commercially clean. The exclusions are deliberate and each has its reason.',
      cards: [
        {
          title: 'In the chain',
          code: 'SDXL              OpenRAIL++\nMV-Adapter        open\nopen3d            Apache-2.0\nspandrel          MIT\nRealESRGAN 6B     BSD-3\nBlender, numpy, scipy, trimesh',
        },
        {
          title: 'Deliberately excluded',
          code: 'nvdiffrast        non-commercial\n                  (enforced by a structural tripwire,\n                   not by attestation)\nHunyuan3D-Paint   licence void in EU / UK / KR\nMVPaint, TEXGen   no licence at all\nUltraSharp, SUPIR non-commercial upscalers\nStableSR',
        },
      ],
    },
  ],
};
