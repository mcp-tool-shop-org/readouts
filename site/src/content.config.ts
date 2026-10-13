import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Newsletter issues carry a date and a few highlights, which the landing page reads.
export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        // YAML reads 2026-10-13 as a Date; keep it as the plain ISO day.
        date: z
          .union([z.string(), z.date()])
          .transform((d) => (typeof d === 'string' ? d : d.toISOString().slice(0, 10)))
          .optional(),
        highlights: z.array(z.string()).optional(),
      }),
    }),
  }),
};
