import React, { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [authState, setAuthState] = useState({
		isLoggedIn: localStorage.getItem("isLoggedIn") === "true",
		username: localStorage.getItem("username") || "",
		isAdmin: localStorage.getItem("isAdmin") === "true",
	});

	// logout function
	const logout = () => {
		localStorage.removeItem("isLoggedIn");
		localStorage.removeItem("username");
		localStorage.removeItem("isAdmin");
		setAuthState({
			isLoggedIn: false,
			username: "",
			isAdmin: false,
		});
	};

	useEffect(() => {
		if (authState.isLoggedIn) {
			localStorage.setItem("isLoggedIn", "true");
			localStorage.setItem("username", authState.username);
			localStorage.setItem(
				"isAdmin",
				authState.isAdmin ? "true" : "false"
			);
		} else {
			localStorage.removeItem("isLoggedIn");
			localStorage.removeItem("username");
			localStorage.removeItem("isAdmin");
		}
	}, [authState]);

	return (
		<AuthContext.Provider value={{ authState, setAuthState, logout }}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => useContext(AuthContext);
