// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://mcp-tool-shop-org.github.io',
  base: '/facet',
  integrations: [
    starlight({
      title: 'facet',
      description: 'A styled 2D concept becomes a textured 3D asset — the handbook.',
      disable404Route: true,
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/mcp-tool-shop-org/facet' },
      ],
      sidebar: [
        {
          label: 'Handbook',
          autogenerate: { directory: 'handbook' },
        },
      ],
      customCss: ['./src/styles/starlight-custom.css'],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
