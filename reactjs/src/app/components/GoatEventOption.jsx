import React, {Component} from 'react';
import Checkbox from 'material-ui/Checkbox';

const styles = {
	row : {
		marginBottom: 8,
	},
	record : {
		color: "grey",
		fontSize: ".9rem"
	},
};

class GoatEventOption extends Component {
	constructor(props) {
		super(props);

	}

	handleClick() {
		//do clicky stuff
		this.props.onClick();
	}


	render() {
		return (
			<div className="row" style={ styles.row } onClick={ () => (this.handleClick()) }>
		    	<div className="col-xs col-sm">
		    		{this.props.teamName}
		    		<span style={styles.record}>
		    			  &nbsp;(3-1)
		    		</span>
		    	</div>
		    	<div className="col-xs-3 col-sm-3">
		    		<Checkbox checked={this.props.picked}/>
		    	</div>

		    </div>
		);
	};
}

export default GoatEventOption;