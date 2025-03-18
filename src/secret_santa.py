import random
from typing import List, Dict, Tuple

import pandas as pd


class SecretSanta:
    """Manages a Secret Santa Game."""

    def __init__(self, team_file: str, past_matches_file: str = None):
        """Initializes with team member data and past pairings.

        Args:
            team_file (str): Path to the Excel file containing team member details.
            past_matches_file (str, optional): Path to the Excel file containing previous Secret Santa pairings.
        """
        self.team_file = team_file
        self.past_matches_file = past_matches_file
        self.team_members = self._get_team_members()
        self.past_matches = self._get_past_members() if past_matches_file else {}

    def _get_team_members(self) -> List[Tuple[str, str]]:
        """Read team members from an Excel file.

        Returns:
            List[Tuple[str, str]]: A list containing team member names and email addresses.

        Raises:
            RuntimeError: If the file cannot be read.
        """
        teams = []
        try:
            df = pd.read_excel(self.team_file)
            for _, row in df.iterrows():
                teams.append((row['Employee_Name'], row['Employee_EmailID']))
        except Exception as e:
            raise RuntimeError(f"Error while loading team members: {e}")
        return teams

    def _get_past_members(self) -> Dict[str, str]:
        """Read past Secret Santa assignments from Excel file

        Returns:
            Dict[str, str]: A dictionary mapping participant emails to their previous gift recipients.

        Raises:
            RuntimeError: If the file cannot be read.
        """
        previous_assignments = {}
        try:
            df = pd.read_excel(self.past_matches_file)
            for _, row in df.iterrows():
                previous_assignments[row['Employee_EmailID']] = row['Secret_Child_EmailID']
        except Exception as e:
            raise RuntimeError(f"Error while reading past match file: {e}")
        return previous_assignments

    def assign_secret_santa(self) -> List[Tuple[str, str, str, str]]:
        """Assigns Secret Santa pairs while avoiding repeats and self-assignments.

        Returns:
            List[Tuple[str, str, str, str]]: A list of pairings, each containing:
                (Member_name, Member_email, receiver_name, receiver_email).

        Raises:
            ValueError: If valid pairings cannot be made due to constraints"""
        participants = self.team_members[:]
        random.shuffle(participants)  # Shuffle to ensure randomness
        pairings = []

        available_children = set(email for _, email in participants)

        for member_name, member_email in participants:
            possible_children = available_children - {member_email}  # Remove self-assignment
            if member_email in self.past_matches:
                possible_children -= {self.past_matches[member_email]}  # Remove last year's assignment

            if not possible_children:
                print("Error: No valid assignments possible.")
                return []

            child_email = random.choice(list(possible_children))
            child_name = next(name for name, email in participants if email == child_email)

            pairings.append((member_name, member_email, child_name, child_email))
            available_children.remove(child_email)

        return pairings

    @staticmethod
    def save_results(result_file: str, pairings: List[Tuple[str, str, str, str]]):
        """Save the assignments to an Excel file.

         Args:
            result_file (str): Path to the output Excel file.
            pairings (List[Tuple[str, str, str, str]]): The list of generated pairings.
        """
        try:
            df = pd.DataFrame(pairings, columns=['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name',
                                                 'Secret_Child_EmailID'])
            df.to_excel(result_file, index=False)
            print(f"Assignments saved to {result_file}")
        except Exception as e:
            raise RuntimeError(f"Error writing output file: {e}")
