import React from "react";
import RadarAnimation from "../Components/RadarAnimation";

const LoginPage = () => {
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
					Login
				</h2>
				<form onSubmit={handleSubmit} className="space-y-4">
					{/* Username */}
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
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your username"
						/>
					</div>

					{/* Password */}
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
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your password"
						/>
					</div>

					<div>
						<button
							type="submit"
							className="w-full px-4 py-2 bg-green-400 text-black font-semibold rounded-md shadow hover:bg-green-500 transition-all duration-300"
						>
							Login
						</button>
					</div>
				</form>
			</div>
		</div>
	);
};

export default LoginPage;
