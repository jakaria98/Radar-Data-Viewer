import React from "react";
import RadarAnimation from "../Components/RadarAnimation";

export default function RegisterUser() {
	const handleRegistration = () => {
		console.log("Registration handling");
	};
	return (
		<div className="min-h-screen flex flex-col justify-center items-center bg-black text-white relative overflow-hidden">
			{/* Background Animation */}
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			{/* Login Form */}
			<div
				className="w-[400px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6 relative z-10"
				style={{
					backdropFilter: "blur(10px)",
					background: "rgba(255, 255, 255, 0.1)",
				}}
			>
				<h2 className="text-2xl font-bold text-green-400 text-center mb-6">
					User Registration
				</h2>
				<form onSubmit={handleRegistration} className="space-y-4">
					<div>
						<label
							htmlFor="name"
							className="block text-green-400 mb-2"
						>
							Name
						</label>
						<input
							type="text"
							id="name"
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your full name"
						/>
					</div>
					<div>
						<label
							htmlFor="username"
							className="block text-green-400 mb-2"
						>
							Username
						</label>
						<input
							type="text"
							id="username"
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your username"
						/>
					</div>

					<div>
						<label
							htmlFor="password"
							className="block text-green-400 mb-2"
						>
							Password
						</label>
						<input
							type="password"
							id="password"
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your password"
						/>
					</div>

					<div>
						<button
							type="submit"
							className="w-full px-4 py-2 bg-green-400 text-black font-semibold rounded-md shadow hover:bg-green-500 transition-all duration-300"
						>
							Register
						</button>
					</div>
				</form>
			</div>
		</div>
	);
}
