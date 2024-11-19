import React, { useEffect, useState } from "react";
import Footer from "../Components/Footer";
import Header from "../Components/Header";

const DataViewer = () => {
	const [sweepAngle, setSweepAngle] = useState(0);

	// Animating the radar sweep
	useEffect(() => {
		const interval = setInterval(() => {
			setSweepAngle((prev) => (prev + 1) % 360);
		}, 50);
		return () => clearInterval(interval);
	}, []);

	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					className="w-[90%] h-[90%] opacity-70"
					viewBox="0 0 100 100"
					preserveAspectRatio="xMidYMid meet"
				>
					{/* Radar Sweeping Beam */}
					<path
						d={`M50 50 L50 0 A50 50 0 0 1 ${
							50 +
							50 * Math.cos((sweepAngle * Math.PI) / 180)
						} ${
							50 -
							50 * Math.sin((sweepAngle * Math.PI) / 180)
						} Z`}
						fill="rgba(0, 255, 0, 0.1)"
					/>
				</svg>
			</div>

			{/* Header */}
			<Header />

			{/* Main Content */}
			<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
				{/* Radar Viewer Container */}
				<div className="w-[700px] bg-black border-4 border-green-500 rounded-lg shadow-xl p-4">
					{/* Upload Button */}
					<div className="text-right mb-4">
						<button className="bg-green-500 text-black px-6 py-2 rounded hover:bg-green-400">
							Upload
						</button>
					</div>

					{/* Radar Viewer */}
					<div className="bg-black border-4 border-green-500 rounded-lg w-full h-[400px] flex justify-center items-center">
						<p className="text-gray-400 text-lg">
							Radar Image Placeholder
						</p>
					</div>

					{/* Video Controls */}
					<div className="flex justify-center items-center mt-4 space-x-4">
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							◀️
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							| |
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							▶️
						</button>
					</div>
				</div>

				{/* Info Box */}
				<div className="w-[700px] bg-black border-4 border-green-500 rounded-lg shadow-xl p-4 mt-8">
					<h2 className="text-xl font-semibold text-green-400 mb-2">
						Image Information
					</h2>
					<p className="text-gray-300">
						This is a placeholder for the radar image's
						metadata or relevant details. You can include
						information like date, time, radar frequency, or
						any additional properties related to the image
						being displayed.
					</p>
				</div>
			</main>

			{/* Footer */}
			<Footer />
		</div>
	);
};

export default DataViewer;
