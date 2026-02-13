import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CLIP Neuron Visualizer',
  description: 'Generate images that maximize neuron activations in CLIP-ViT-B/32',
  openGraph: {
    title: 'CLIP Neuron Visualizer',
    description: 'Visualize what different neurons in CLIP respond to',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
