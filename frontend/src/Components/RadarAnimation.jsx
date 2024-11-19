import React, { useEffect, useState } from "react";

const RadarAnimation = () => {
	const [sweepAngle, setSweepAngle] = useState(0);

	// Increment the sweep angle
	useEffect(() => {
		const interval = setInterval(() => {
			setSweepAngle((prev) => (prev + 1) % 360);
		}, 50);
		return () => clearInterval(interval);
	}, []);

	// Utility function to generate concentric circles
	const renderCircles = () => {
		const circles = [];
		for (let i = 1; i <= 4; i++) {
			circles.push(
				<circle
					key={i}
					cx="50"
					cy="50"
					r={i * 12.5}
					stroke="rgba(0, 255, 0, 0.1)"
					strokeWidth="0.25"
					fill="none"
				/>
			);
		}
		return circles;
	};

	// Utility function to generate angle markings
	const renderAngleLines = () => {
		const lines = [];
		for (let i = 0; i < 360; i += 30) {
			const x1 = 50 + 48 * Math.cos((i * Math.PI) / 180);
			const y1 = 50 - 48 * Math.sin((i * Math.PI) / 180);
			const x2 = 50 + 50 * Math.cos((i * Math.PI) / 180);
			const y2 = 50 - 50 * Math.sin((i * Math.PI) / 180);
			lines.push(
				<line
					key={i}
					x1={x1}
					y1={y1}
					x2={x2}
					y2={y2}
					stroke="rgba(0, 255, 0, 0.1)"
					strokeWidth="0.25"
				/>
			);
		}
		return lines;
	};

	return (
		<svg
			xmlns="http://www.w3.org/2000/svg"
			className="w-full h-full"
			viewBox="0 0 100 100"
			preserveAspectRatio="xMidYMid meet"
		>
			{/* Background */}
			<rect width="100" height="100" fill="black" />

			{/* Radar Circles */}
			{renderCircles()}

			{/* Angle Markings */}
			{renderAngleLines()}

			{/* Radar Sweep Beam */}
			<path
				d={`M50 50 L50 0 A50 50 0 0 1 ${
					50 + 50 * Math.cos((sweepAngle * Math.PI) / 180)
				} ${50 - 50 * Math.sin((sweepAngle * Math.PI) / 180)} Z`}
				fill="rgba(0, 255, 0, 0.1)"
			/>

			{/* Radar Center Dot */}
			<circle cx="50" cy="50" r="1" fill="lime" />
		</svg>
	);
};

export default RadarAnimation;
