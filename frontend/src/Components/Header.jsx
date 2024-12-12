import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const Header = () => {
	const { authState, logout } = useAuth();
	const navigate = useNavigate();

	const [isMenuOpen, setIsMenuOpen] = useState(false);

	const handleLogout = () => {
		logout();
		navigate("/login");
	};

	const toggleMenu = () => {
		setIsMenuOpen((prevState) => !prevState);
	};

	const handleNavigation = (path) => {
		navigate(path);
		setIsMenuOpen(false);
	};

	return (
		<header className="bg-headerFooter border-b-2 border-green-400 py-4 top-0 w-full z-20 relative">
			<div className="px-4 flex justify-between">
				<h1 className="text-3xl font-bold text-green-400">
					Radar Data Viewer
				</h1>
				<div className="flex items-center gap-4">
					<p className="text-green-400">
						Hi,{" "}
						{authState.isAdmin
							? "Super Admin"
							: authState.username}
					</p>
					<button
						className="glass-button px-4 py-2"
						onClick={toggleMenu}
					>
						<span className="text-green-400">=</span>
					</button>

					{isMenuOpen && (
						<div className="absolute right-4 top-16 bg-black text-white border border-green-400 shadow-lg p-4 w-40 z-30">
							<ul className="space-y-2">
								<li
									className="cursor-pointer hover:bg-green-400 text-green-400 hover:text-black text-center py-2"
									onClick={() =>
										handleNavigation("/home")
									}
								>
									Home
								</li>

								<li
									className="cursor-pointer hover:bg-green-400 text-green-400 hover:text-black text-center py-2"
									onClick={() =>
										handleNavigation("/upload")
									}
								>
									Upload
								</li>

								{authState.isAdmin && (
									<>
										<li
											className="cursor-pointer hover:bg-green-400 text-green-400 hover:text-black text-center py-2"
											onClick={() =>
												handleNavigation(
													"/register"
												)
											}
										>
											Add User
										</li>

										<li
											className="cursor-pointer hover:bg-green-400 text-green-400 hover:text-black text-center py-2"
											onClick={() =>
												handleNavigation(
													"/all-users"
												)
											}
										>
											All Users
										</li>
									</>
								)}

								{authState.isLoggedIn && (
									<li
										className="cursor-pointer hover:bg-green-400 text-green-400 hover:text-black text-center py-2"
										onClick={() =>
											handleNavigation(
												"/history"
											)
										}
									>
										History
									</li>
								)}
								<li className="cursor-pointerpy-2">
									<button
										className="glass-button w-full"
										onClick={handleLogout}
									>
										Logout
									</button>
								</li>
							</ul>
						</div>
					)}
				</div>
			</div>
		</header>
	);
};

export default Header;
