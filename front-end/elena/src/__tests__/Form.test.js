import React from "react";
import NavForm from '../Components/Form';
import { create } from 'react-test-renderer';
import { render, cleanup } from "@testing-library/react";
import { screen, fireEvent} from "@testing-library/dom";



describe("Form snapshot should match", () => {
    it("Matches DOM Snapshot", () => {
      const domTree = create(<NavForm />).toJSON();
      expect(domTree).toMatchSnapshot();
    });
});

// it('On submit Metrics table should be mounted', () => {
//     const { getByText, getByDisplayValue, container } = render(<NavForm setRoute={()=>{}} /> );
//     //expect(getByText("ROUTE INFORMATION")).not.toBeInTheDocument()
//     let table = container.querySelector(".metrictable-container");
//     expect(table).toBe(null);
//     fireEvent.click(getByText("Go!"));
//     table = container.querySelector(".metrictable-container");
//     expect(screen.getByText("ROUTE INFORMATION")).toBeInTheDocument();
//     cleanup()
// });