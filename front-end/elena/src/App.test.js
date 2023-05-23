import { render, screen } from '@testing-library/react';
import App from './App';
import React from "react";
import renderer from "react-test-renderer";

// test('renders learn react link', () => {
//   render(<App />);
//   const linkElement = screen.getByText(/Elena/i);
//   expect(linkElement).toBeInTheDocument();
// });

describe("App snapshot should match", () => {
  it("Matches DOM Snapshot", () => {
    const domTree = renderer.create(<App />).toJSON();
    expect(domTree).toMatchSnapshot();
  });
});

// it('On submit Metrics table should be mounted', () => {
//   const { getByText, getByDisplayValue, container } = render(< App></App> );
//   //expect(getByText("ROUTE INFORMATION")).not.toBeInTheDocument()
//   let table = container.querySelector(".metrictable-container");
//   expect(table).toBe(null);
//   fireEvent.click(getByText("Go!"));
//   table = container.querySelector(".metrictable-container");
//   expect(screen.getByText("ROUTE INFORMATION")).toBeInTheDocument();
//   cleanup()
// });