import React, {Component} from 'react';

import Paper from 'material-ui/Paper';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';

class YourGOATIndex extends Component {
	constructor(props) {
		super(props);

		this.state= {

		};
	}

	renderOverallIndex() {
		return (
			<Paper style={ { marginTop: 8 } }>
				<Table>
					<TableHeader adjustForCheckbox={false} displaySelectAll={false}>
						<TableRow>
						 	<TableHeaderColumn tooltip="Sport">Sport</TableHeaderColumn>
						 	<TableHeaderColumn tooltip="Correct">Correct</TableHeaderColumn>
						 	<TableHeaderColumn tooltip="Total">Total</TableHeaderColumn>
						 	<TableHeaderColumn tooltip="Percent">Percent</TableHeaderColumn>
						</TableRow>
					</TableHeader>

					<TableBody displayRowCheckbox={false}>
						<TableRow>
							<TableRowColumn>Overall</TableRowColumn>	
							<TableRowColumn>{ this.props.goat_indeces.overall.correct }</TableRowColumn>
        					<TableRowColumn>{ this.props.goat_indeces.overall.total }</TableRowColumn>
        					<TableRowColumn>{ 100 * this.props.goat_indeces.overall.correct / this.props.goat_indeces.overall.total}</TableRowColumn>
						</TableRow>
					</TableBody>
				</Table>


			</Paper>
		);
	}

	render() {
		return (
			this.renderOverallIndex()
		);
	}
}

export default YourGOATIndex;