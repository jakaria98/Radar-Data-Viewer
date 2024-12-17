import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

const AllUsers = () => {
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

	const [users, setUsers] = useState([]);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchUsers = async () => {
			try {
				const response = await fetch(
					"http://127.0.0.1:8000/api/allusers/"
				);
				const data = await response.json();
				if (response.ok) {
					setUsers(data.users);
				} else {
					setError(data.message || "Failed to fetch users.");
				}
			} catch (err) {
				setError("An error occurred while fetching users.");
			}
		};

		fetchUsers();
	}, []);

	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<Header />

			<main className="flex-grow flex flex-col items-center justify-center py-8 relative z-10">
				<h1 className="text-4xl font-bold text-green-400 mb-8 text-center">
					Users List
				</h1>

				{error && (
					<div className="text-red-500 bg-black border border-red-500 rounded-lg p-4 mb-4">
						{error}
					</div>
				)}

				<div
					className="w-[90%] max-w-4xl bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<table className="w-full text-left border-separate border-spacing-y-4">
						<thead
							className="bg-glass text-white font-medium shadow-glass"
							style={{
								backdropFilter: "blur(10px)",
								background: "rgba(255, 255, 255, 0)",
							}}
						>
							<tr>
								<th className="px-6 py-4">
									First Name
								</th>
								<th className="px-6 py-4">Last Name</th>
								<th className="px-6 py-4">Email</th>
								<th className="px-6 py-4">Username</th>
							</tr>
						</thead>
						<tbody>
							{users.length > 0 ? (
								users.map((user, index) => (
									<tr
										key={index}
										className="bg-glass text-green-400 shadow-glass hover:text-white"
										style={{
											backdropFilter:
												"blur(10px)",
											background:
												"rgba(255, 255, 255, 0)",
										}}
									>
										<td className="px-6 py-4">
											{user.is_staff
												? `*  ${
														user.first_name ||
														"-"
												  }`
												: `${
														user.first_name ||
														"-"
												  }`}
										</td>
										<td className="px-6 py-4">
											{user.last_name || "-"}
										</td>
										<td className="px-6 py-4">
											{user.email || "-"}
										</td>
										<td className="px-6 py-4">
											{user.username || "-"}
										</td>
									</tr>
								))
							) : (
								<tr>
									<td
										colSpan="4"
										className="px-6 py-4 text-center text-gray-400"
									>
										No users available
									</td>
								</tr>
							)}
						</tbody>
					</table>
				</div>
			</main>

			<Footer />
		</div>
	);
};

export default AllUsers;
