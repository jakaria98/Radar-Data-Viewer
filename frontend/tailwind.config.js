/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				radarGreen: "#00ff00",
			},
			boxShadow: {
				radar: "0 0 10px #00ff00, 0 0 20px #00ff00",
			},
		},
	},
	plugins: [],
};
