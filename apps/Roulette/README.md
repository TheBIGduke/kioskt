# Premium Roulette

A visually stunning, animated roulette wheel built with HTML, CSS, and JavaScript. Designed to let users spin and win prizes with a realistic spinning effect.

---

# Premium Roulette

A visually stunning, animated roulette wheel built with HTML, CSS, and JavaScript. Designed to let users spin and win prizes with a realistic spinning effect.

---

## Configuration

All settings, including prizes, UI, and audio, are managed in `config.js`.

### How to Add New Prizes (Segments)

1.  Open `config.js`.
2.  Locate the `prizes` array in the `GAME_CONFIG` object.
3.  Add a new prize object:

```js
{
  "number": 9,
  "color": "segmentA",
  "label": "Playera Edición Especial",
  "weight": 8
}
```

Make sure:
- `number`: Unique and sequential.
- `color`: `'segmentA'` (red by default) or `'segmentB'` (black/dark by default).
- `label`: The text displayed on the wheel.
- `weight`: Chance of winning (higher = more likely).

---

## Customization

You can also customize the UI and Audio in `config.js`:

- **UI**: Change the title, logo, and colors.
- **Wheel**: Adjust the text size, spin duration, and colors.
- **Audio**: Set a custom spin sound path.

---

## Important Notes

- The wheel redraws itself dynamically based on `config.js`.
- No need to edit `index.html` directly for content changes.


