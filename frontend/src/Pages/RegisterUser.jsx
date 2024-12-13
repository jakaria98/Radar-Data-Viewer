import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

export default function RegisterUser() {
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [email, setEmail] = useState("");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const [message, setMessage] = useState("");

	const navigate = useNavigate();
	const { authState } = useAuth();
	useEffect(() => {
		console.log(authState.isAdmin);
		// if not logged in or not admin
		if (!authState.isLoggedIn) {
			console.log("Not Logged In");
			navigate("/login");
			return;
		}

		if (authState.isAdmin === false) {
			console.log("not admin");
			navigate("/");
			return;
		}
	}, [authState.isLoggedIn, authState.isAdmin, navigate]);

	const handleRegistration = async (e) => {
		e.preventDefault();

		if (!firstName || !lastName || !email || !username || !password) {
			setMessage("Please enter the required values.");
			return;
		}

		try {
			const response = await fetch(
				"http://127.0.0.1:8000/api/register/",
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						first_name: firstName,
						last_name: lastName,
						email,
						username,
						password,
					}),
				}
			);

			const data = await response.json();

			if (response.ok) {
				setMessage("User added successfully!");
				console.log("Response: ", data);

				navigate("/all-users");
			} else {
				setMessage(data.message || "Invalid data!");
			}
		} catch (error) {
			console.error("Error: ", error);
			setMessage("Error adding new user");
		}
	};
	return (
		<div className="min-h-screen flex flex-col justify-center items-center bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<Header />

			<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
				<div
					className="w-[400px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-2 relative z-10 mb-4"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<h2 className="text-2xl font-bold text-green-400 text-center">
						User Registration
					</h2>
				</div>
				<div
					className="w-[400px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6 relative z-10"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<form
						onSubmit={handleRegistration}
						className="space-y-4"
					>
						<div className="flex gap-4">
							<div>
								<label
									htmlFor="firstName"
									className="block text-green-400 mb-2"
								>
									First Name
								</label>
								<input
									type="text"
									id="firstName"
									value={firstName}
									onChange={(e) =>
										setFirstName(e.target.value)
									}
									className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
									placeholder="First Name"
								/>
							</div>
							<div>
								<label
									htmlFor="lastName"
									className="block text-green-400 mb-2"
								>
									Last Name
								</label>
								<input
									type="text"
									id="lastName"
									value={lastName}
									onChange={(e) =>
										setLastName(e.target.value)
									}
									className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
									placeholder="Last Name"
								/>
							</div>
						</div>
						<div>
							<label
								htmlFor="email"
								className="block text-green-400 mb-2"
							>
								Email Address
							</label>
							<input
								type="email"
								id="email"
								value={email}
								onChange={(e) =>
									setEmail(e.target.value)
								}
								className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
								placeholder="Enter your email address"
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
								value={username}
								onChange={(e) =>
									setUsername(e.target.value)
								}
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
								value={password}
								onChange={(e) =>
									setPassword(e.target.value)
								}
								className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
								placeholder="Enter your password"
							/>
						</div>

						<div>
							<button
								type="submit"
								className="w-full px-4 py-2 bg-green-400 text-black font-medium rounded-md shadow hover:bg-green-500 transition-all duration-300"
							>
								Register
							</button>
						</div>
					</form>
				</div>
			</main>

			<Footer />
		</div>
	);
}
