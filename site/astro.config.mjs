// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://mcp-tool-shop-org.github.io',
  base: '/readouts',
  integrations: [
    starlight({
      title: 'readouts',
      description:
        'How to query, trust and maintain readouts: verified, source-backed SQLite knowledge bases.',
      // Starlight links the header title to the base path, which is the landing page.
      logo: {
        src: './src/assets/logo.png',
        alt: 'readouts',
        replacesTitle: false,
      },
      disable404Route: true,
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/mcp-tool-shop-org/readouts' },
      ],
      sidebar: [
        {
          label: 'Handbook',
          items: [{ autogenerate: { directory: 'handbook' } }],
        },
      ],
      customCss: ['./src/styles/starlight-custom.css'],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
