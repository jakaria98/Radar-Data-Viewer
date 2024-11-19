import React, { useEffect, useState } from "react";

const BackgroundAnimation = () => {
	const [sweepAngle, setSweepAngle] = useState(0);

	// Animating the radar sweep
	useEffect(() => {
		const interval = setInterval(() => {
			setSweepAngle((prev) => (prev + 1) % 360);
		}, 50);
		return () => clearInterval(interval);
	}, []);
	return (
		<svg
			xmlns="http://www.w3.org/2000/svg"
			className="w-[90%] h-[90%] opacity-70"
			viewBox="0 0 100 100"
			preserveAspectRatio="xMidYMid meet"
		>
			{/* Radar Sweeping Beam */}
			<path
				d={`M50 50 L50 0 A50 50 0 0 1 ${
					50 + 50 * Math.cos((sweepAngle * Math.PI) / 180)
				} ${50 - 50 * Math.sin((sweepAngle * Math.PI) / 180)} Z`}
				fill="rgba(0, 255, 0, 0.1)"
			/>
		</svg>
	);
};

export default BackgroundAnimation;
