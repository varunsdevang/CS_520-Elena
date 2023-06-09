import { render, screen } from '@testing-library/react';
import React from "react";
import renderer from "react-test-renderer";
import MetricTable from '../Components/Metrics';


describe("Metrics table snapshot should match", () => {
    it("Matches DOM Snapshot", () => {
      const domTree = renderer.create(< MetricTable elevation={1000} distance={1000} time={1000} mode={'drive'}/>).toJSON();
      expect(domTree).toMatchSnapshot();
    });
});